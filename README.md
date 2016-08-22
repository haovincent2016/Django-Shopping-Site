## Django-Shopping-Site (using python 3.4 + django 1.9)
## For Demo:
- Dependency: python 3 + django 1.9
- This proj is a mock shopping website with pages for both buyers and sellers
- The main function includes: 
  1. buyer: view/search product, place order
    * pages: store page / order(new/history) / cart
    * catalog page <==> cart page / order ==> checkout ==> receipt(pending)
  2. seller: organize product, handle order, product delivery
    * pages: admin site / list / product organization(createsuperuser to login) / order processing
    * login ==> product organization page(view/add/edit/delete)==> pending order(handle/ignore)
