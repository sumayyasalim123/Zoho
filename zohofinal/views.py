from io import BytesIO
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.db.models import Sum
from django.template.loader import get_template
from django.conf import settings
from .models import LoginDetails, CompanyDetails, StaffDetails, ZohoModules, Items, SalesOrderItems
from django.contrib import messages
from xhtml2pdf import pisa




def stock_summary(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        log_details = LoginDetails.objects.get(id=log_id)
        if log_details.user_type == 'Company':
            cmp = CompanyDetails.objects.get(login_details=log_details)
            dash_details = CompanyDetails.objects.get(login_details=log_details)
        else:
            cmp = StaffDetails.objects.get(login_details=log_details).company
            dash_details = StaffDetails.objects.get(login_details=log_details)

        allmodules = ZohoModules.objects.get(company=cmp)

        # Fetch items related to the company
        items = Items.objects.filter(company=cmp)
        item_data = []
        for item in items:
            # Calculate the total quantity sold for each item
            total_quantity_sold = SalesOrderItems.objects.filter(
                item=item, company=cmp
            ).aggregate(total_quantity_sold=Sum('quantity'))['total_quantity_sold'] or 0

            difference = item.current_stock - total_quantity_sold
            item_data.append({
                'item_name': item.item_name,
                'opening_stock': item.opening_stock,
                'quantity_sold': total_quantity_sold,
                'difference': difference,
            })

        context = {
            'cmp': cmp,
            'details': dash_details,
            'log_details': log_details,
            'items': item_data,
            'allmodules': allmodules
        }
        return render(request, 'zohomodules/Reports/stock_summary.html', context)
    else:
        # Handle the case when the user is not logged in
        return redirect('/')








def customize_stock_summary(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        log_details = LoginDetails.objects.get(id=log_id)
        if log_details.user_type == 'Company':
            cmp = CompanyDetails.objects.get(login_details=log_details)
            dash_details = CompanyDetails.objects.get(login_details=log_details)
        else:
            cmp = StaffDetails.objects.get(login_details=log_details).company
            dash_details = StaffDetails.objects.get(login_details=log_details)

        allmodules = ZohoModules.objects.get(company=cmp)

        # Get date range from request
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')

        # Fetch items related to the company
        items = Items.objects.filter(company=cmp)
        item_data = []

        for item in items:
            # Filter SalesOrderItems based on date range if provided
            sales_order_items_query = SalesOrderItems.objects.filter(item=item, company=cmp)
            if from_date and to_date:
                sales_order_items_query = sales_order_items_query.filter(
                    sales_order__sales_order_date__range=[from_date, to_date]
                )
            total_quantity_sold = sales_order_items_query.aggregate(
                total_quantity_sold=Sum('quantity')
            )['total_quantity_sold'] or 0

            difference = item.current_stock - total_quantity_sold
            item_data.append({
                'item_name': item.item_name,
                'opening_stock': item.opening_stock,
                'quantity_sold': total_quantity_sold,
                'difference': difference,
            })

        context = {
            'cmp': cmp,
            'details': dash_details,
            'log_details': log_details,
            'items': item_data,
            'allmodules': allmodules,
            'from_date': from_date,
            'to_date': to_date,
        }
        return render(request, 'zohomodules/Reports/stock_summary.html', context)
    else:
        # Handle the case when the user is not logged in
        return redirect('/')


def shareStockSummaryToEmail(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        log_details= LoginDetails.objects.get(id=log_id)
        if log_details.user_type == 'Company':
            cmp = CompanyDetails.objects.get(login_details = log_details)
            dash_details = CompanyDetails.objects.get(login_details=log_details)
        else:
            cmp = StaffDetails.objects.get(login_details = log_details).company
            dash_details = StaffDetails.objects.get(login_details=log_details)


            allmodules = ZohoModules.objects.filter(company=cmp, status='New')

        try:
            if request.method == 'POST':
                emails_string = request.POST['email_ids']

                # Split the string by commas and remove any leading or trailing whitespace
                emails_list = [email.strip() for email in emails_string.split(',')]
                email_message = request.POST['email_message']

               
                from_date = request.POST['start']
                to_date = request.POST['end']
               

                
                if from_date and to_date:
                    items = Items.objects.filter(salesorderitems__sales_order__sales_order_date__range=[from_date, to_date]).filter(company=cmp).distinct()

                    
                    item_data = []
                    for item in items:
                        total_quantity_sold = SalesOrderItems.objects.filter(
                            item=item, sales_order__sales_order_date__range=[from_date, to_date]
                        ).aggregate(total_quantity_sold=Sum('quantity'))['total_quantity_sold'] or 0

                        difference = item.current_stock - total_quantity_sold
                        item_data.append({
                            'item_name': item.item_name,
                            'opening_stock': item.opening_stock,
                            'quantity_sold': total_quantity_sold,
                            'difference': difference,
                            
                        })

                  
                context = { 'items': item_data,
                        'from_date': from_date,
                        'to_date': to_date,
                        'cmp': cmp,
                        'details': dash_details,
                        'log_details': log_details,
                   }
                template_path = 'zohomodules/Reports/stock_summary_Pdf.html'
                template = get_template(template_path)

                html  = template.render(context)
                result = BytesIO()
                pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
                pdf = result.getvalue()
                filename = f'stock summary report'
                subject = f"stock summary Report"
                # from django.core.mail import EmailMessage as EmailMsg
                email = EmailMsg(subject, f"Hi,\nPlease find the attached Sales By Report. \n{email_message}\n\n--\nRegards,\n{cmp.company_name}\n{cmp.address}\n{cmp.state} - {cmp.country}\n{cmp.contact}", from_email=settings.EMAIL_HOST_USER, to=emails_list)
                email.attach(filename, pdf, "application/pdf")
                email.send(fail_silently=False)

                messages.success(request, 'Sales By Report details has been shared via email successfully..!')
                return redirect(stock_summary)
        except Exception as e:
            print(e)
            messages.error(request, f'{e}')
            return redirect(stock_summary)
