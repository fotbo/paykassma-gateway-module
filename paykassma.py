import json
import logging
from rest_framework import status
from django.shortcuts import render
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect, HttpRequest
from common.core.formatting.currency_formatter import format_currency
from common.rest_framework.authentication.token_authentication import generate_otp_token_for_request

from fleio.billing.gateways.decorators import gateway_action
from fleio.billing.gateways import exceptions as gateway_exceptions
from fleio.billing.models import Invoice
from ...invoicing.serializers import InvoiceItemSerializer

from .operations import PaymentProcess
from .services import Payment
from .conf import conf


LOG = logging.getLogger(__name__)

payment = Payment(
    api_key=conf.api_key,
    api_url=conf.api_url)


def validate_invoice(invoice_id: int) -> None | Exception:
    inv = Invoice.objects.get(pk=invoice_id)
    if inv.balance <= 0 and inv.status == 'paid':
        LOG.info(f'Invoice {invoice_id} is already paid')
        raise gateway_exceptions.InvoicePaymentException(
            f'Invoice {invoice_id} is already paid')


def return_pay_message(invoice: Invoice, request: HttpRequest) -> str:
    amount = str(invoice.balance)
    localized_amount = format_currency(
        amount=amount,
        currency_code=invoice.currency.pk,
        locale=request.user.language)
    pay_message = _('Pay {} for invoice {}'.format(localized_amount, invoice.pk))
    return pay_message

@gateway_action(methods=['GET'])
def pay_invoice(request: HttpRequest) -> HttpResponseRedirect:
    invoice_id = request.query_params.get('invoice')
    if invoice_id is None:
        LOG.error("An 'invoice' parameter is required")
        raise gateway_exceptions.GatewayException("An 'invoice' parameter is required")
    try:
        inv = Invoice.objects.get(pk=invoice_id, client=request.user.get_active_client(request=request))
    except Invoice.DoesNotExist:
        LOG.error('Invoice {} does not exist'.format(invoice_id))
        raise gateway_exceptions.GatewayException('Invoice {} does not exist'.format(invoice_id))
    if inv.balance <= 0:
        LOG.info('Invoice {} is already paid'.format(invoice_id), invoice_id=invoice_id)
        raise gateway_exceptions.InvoicePaymentException('Invoice {} is already paid'.format(invoice_id), invoice_id=invoice_id)

    return render(
        template_name='paykassma/pay_invoice.html',
        request=request,
        context={
            'pay_message': return_pay_message(inv, request),
            'company_info': inv.client.billing_settings.company_info,
            'invoice_items': InvoiceItemSerializer(instance=inv.items, many=True).data,
            'invoice_taxes': inv.taxes,
            'invoice_id': inv.pk,
            'invoice_url': inv.frontend_url,
            'invoice_total': inv.total,
            'invoice_subtotal': inv.subtotal,
            'invoice_balance': inv.balance,
            'payment_systems': json.dumps({
                'payments': conf.payment_systems
            }),
            'token': generate_otp_token_for_request(request=request),
        }
        )

@gateway_action(methods=['POST'])
def charge(request: HttpRequest):
    user = request.user.get_active_client(request=request)
    currency_id = request.data.get('currency')
    try:
        res = payment.create(
            amount=request.data.get('converted_value'),
            currency=currency_id,
            invoice_id=request.GET.get('invoice'),
            user_id=user.pk,
            return_url=conf.return_url,
            webhook_id=conf.webhook_id,
            payment_system=conf.get_payment_system(currency_id)
        )
        return HttpResponseRedirect(res)
    except Exception as err:
        LOG.error(f"Payment error - {err}")
        return Response(
            {'detail': 'Error'},
            status=status.HTTP_400_BAD_REQUEST)

@gateway_action(methods=['POST'])
def callback(request: HttpRequest) -> Response:
    try:
        invoice_id = request.data.get('order_id')
        validate_invoice(invoice_id)
        payment_process = PaymentProcess(rq_data=request.data)
        payment_process.process_charge()
        return Response({'detail': 'OK'}, status=status.HTTP_200_OK)
    except Exception as err:
        LOG.error(f"Payment error - {err}")
        return Response(
            {'detail': 'Error'},
            status=status.HTTP_400_BAD_REQUEST)
