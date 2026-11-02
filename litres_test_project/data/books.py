import dataclasses
import re


@dataclasses.dataclass
class Book:
    name: str
    author: str
    price: str
    url: str

    @property
    def id(self) -> str:
        # 'andzhey-sapkovskiy/vedmak-6375365/' -> '6375365'
        match = re.search(r'-(\d+)/?$', self.url)
        if not match:
            raise ValueError(f'Cannot extract book id from url: {self.url!r}')
        return match.group(1)

    @property
    def price_aria(self) -> str:
        # '1 599 ₽' -> '1599 RUB' (значение aria-label цены на сайте)
        return f"{re.sub(r'\D', '', self.price)} RUB"