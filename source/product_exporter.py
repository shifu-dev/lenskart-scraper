class product_exporter:
    def __init__(self, writer):
        self.writer = writer
        writer.writerow(["Title", "Price", "Currency Type", "Size"])

    def add(self, product):
        self.writer.writerow(
            [
                product.title,
                product.price,
                product.currency,
                product.size,
            ]
        )

    writer: any
