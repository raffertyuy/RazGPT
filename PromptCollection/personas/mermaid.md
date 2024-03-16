```mermaid
classDiagram
  Order "1" --> "*" LineItem : contains
  Order : +addLineItem(LineItem)
  Order : +getLineItems()
  Order : +getTotalAmount()
  Order : +getStatus()
  OrderStatus : RECEIVED
  OrderStatus : REJECTED
  OrderStatus : ACCEPTED
  LineItem : +getItemId()
  LineItem : +getItemPrice()
  LineItem : +getItemQuantity()