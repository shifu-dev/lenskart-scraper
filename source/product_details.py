class Details:
    product_title = ""
    product_price = 0
    product_currency = ""
    product_size = ""

    def __str__(self) -> str:
        result = (
            f"product_title: {self.product_title}\n"
            f"product_price: {self.product_price}\n"
            f"product_currency: {self.product_currency}\n"
            f"product_size: {self.product_size}\n"
        )

        return result
