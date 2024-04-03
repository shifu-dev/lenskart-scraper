class product_exporter:
    def __init__(self, writer):
        self.writer = writer
        writer.writerow(["Title", "Price", "Currency Type", "Size"])

    def add(self, product):
        self.writer.writerow(
            [
                product.product_title,
                product.product_price,
                product.product_currency,
                product.product_size,
            ]
        )

    writer: any
