class Details:
    product_title = ""
    product_collection = ""
    product_size = ""
    product_price = 0
    discounted_price = ""
    coupen_code = ""
    product_rating = ""

    def __str__(self) -> str:
        result = (
            f"product_title: {self.product_title}\n"
            f"product_collection: {self.product_collection}\n"
            f"product_size: {self.product_size}\n"
            f"product_price: {self.product_price}\n"
            f"discounted_price: {self.discounted_price}\n"
            f"coupen_code: {self.coupen_code}\n"
            f"product_rating: {self.product_rating}\n"
        )

        return result
