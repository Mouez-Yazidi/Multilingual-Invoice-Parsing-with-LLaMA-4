# models.py
from pydantic import BaseModel, Field
from typing import List, Optional

class LineItem(BaseModel):
    description: Optional[str] = Field(
        None, description="A brief description of the product or service provided."
    )
    quantity: Optional[float] = Field(
        None, description="The number of units of the product or service."
    )
    unit_price: Optional[float] = Field(
        None, description="The price per unit of the product or service."
    )
    total_price: Optional[float] = Field(
        None, description="The total price for the line item, calculated as quantity × unit price."
    )

class InvoiceData(BaseModel):
    invoice_number: Optional[str] = Field(
        None, description="The unique identifier or reference number of the invoice."
    )
    invoice_date: Optional[str] = Field(
        None, description="The date when the invoice was issued."
    )
    due_date: Optional[str] = Field(
        None, description="The payment due date."
    )
    billing_address: Optional[str] = Field(
        None, description="The address of the customer who is being billed."
    )
    shipping_address: Optional[str] = Field(
        None, description="The address where the goods/services are to be delivered."
    )
    vendor_name: Optional[str] = Field(
        None, description="The name of the company or individual issuing the invoice."
    )
    customer_name: Optional[str] = Field(
        None, description="The name of the person or organization being billed."
    )
    line_items: Optional[List[LineItem]] = Field(
        None, description="A list of items described in the invoice."
    )
    subtotal: Optional[float] = Field(
        None, description="The sum of all line item totals before taxes or additional fees."
    )
    tax: Optional[float] = Field(
        None, description="The tax amount applied to the subtotal."
    )
    total_amount: Optional[float] = Field(
        None, description="The final total to be paid including subtotal and taxes."
    )
    currency: Optional[str] = Field(
        None, description="The currency in which the invoice is issued (e.g., USD, EUR)."
    )
