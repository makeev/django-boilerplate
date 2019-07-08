import os
import math
import random
import string
import binascii
import collections

from datetime import timedelta

import names

from faker import Faker
from PIL import Image, ImageDraw
from transliterate import translit
from django.utils.text import slugify

import sha3

RGBColor = collections.namedtuple('RGBColor', ['red', 'green', 'blue'])
letters = list(string.ascii_uppercase)+list(string.ascii_lowercase)
digits = list(string.digits)


def generate_first_name(gender=None):
    return names.get_first_name(gender)


def generate_last_name(gender=None):
    return names.get_last_name(gender)


def generate_full_name(gender=None):
    return names.get_full_name(gender)


def generate_username(fullname=None):
    """
    Можно передать fullname, чтобы username был похож на имя пользователя
    """
    if not fullname:
        fullname = generate_full_name()
    first_name, last_name = fullname.split(" ")
    fname_postfix = "".join(random.sample(digits+letters, random.randint(1, 2)))
    lname_postfix = "".join(random.sample(digits+letters, random.randint(1, 2)))

    return '{first_name}{fname_postfix}{last_name}{lname_postfix}'.format(
        first_name=first_name,
        last_name=last_name,
        fname_postfix=fname_postfix,
        lname_postfix=lname_postfix
    )


def generate_random_email(username=None):
    if not username:
        username = generate_username()

    return '%s@%s' % (
        username,
        random.choice(['yandex.com', 'gmail.com', 'mail.com', 'mail.ru', 'yahoo.com'])
    )


def generate_random_eth_address():
    def checksum_encode(addr):
        o = ''
        v = sha3.keccak_256(addr.lower().encode()).hexdigest()
        for i, c in enumerate(addr):
            o += c.lower() if int(v[i], 16) < 8 else c.upper()
        return o
    # это всё ядски медленно
    # priv = SigningKey.generate(curve=SECP256k1)
    # pub = priv.get_verifying_key().to_string()
    # address = sha3.keccak_256(pub).hexdigest()[24:]
    address = binascii.b2a_hex(os.urandom(20)).decode()
    return '0x%s' % checksum_encode(address)


def generate_random_blog_post(lang=None):
    """
    Генератор фейковых новостей
    Возвращает словарь из title, slug, annotation, text
    @TODO переделать во что-то более универсальное
    """
    if lang is None:
        lang = 'en_US'

    fake = Faker(lang)

    title = fake.sentence()
    slug = title
    if lang != 'en_US':
        slug = translit(slug, reversed=True)
    slug = slugify(slug) + "".join(random.sample(digits+letters, random.randint(1, 2)))

    return {
        'title': title,
        'slug': slug,
        'annotation': fake.text(),
        'text': "\n".join(fake.paragraphs())
    }


def generate_random_image(x, y):
    """
    Generate the shapes and colors, and draw them on the canvas
    """
    def _hsv_to_rgb(h, s, v):
        if s == 0.0:
            return v, v, v
        i = int(h*6.0)
        f = (h*6.0) - i
        p = int(v*(1.0 - s))
        q = int(v*(1.0 - s*f))
        t = int(v*(1.0 - s*(1.0-f)))
        i = i % 6
        if i == 0:
            return v, t, p
        if i == 1:
            return q, v, p
        if i == 2:
            return p, v, t
        if i == 3:
            return p, q, v
        if i == 4:
            return t, p, v
        if i == 5:
            return v, p, q

    def _scale_coordinates(generator, image_width, image_height, side_length=50):
        scaled_width = int(image_width / side_length) + 1
        scaled_height = int(image_height / side_length) + 1
        for coords in generator(scaled_width, scaled_height):
            yield [(x * side_length, y * side_length) for (x, y) in coords]

    def _generate_unit_triangles(image_width, image_height):
        h = math.sin(math.pi / 3)
        for x in range(-1, image_width):
            for y in range(int(image_height / h)):
                x_ = x if (y % 2 == 0) else x + 0.5
                yield [(x_, y * h), (x_ + 1, y * h), (x_ + 0.5, (y + 1) * h)]
                yield [(x_ + 1, y * h), (x_ + 1.5, (y + 1) * h), (x_ + 0.5, (y + 1) * h)]

    def _generate_triangles(*args, **kwargs):
        return _scale_coordinates(_generate_unit_triangles, *args, **kwargs)

    def random_color(start, end):
        while True:
            chosen_d = random.uniform(0, 1)
            yield RGBColor(
                start.red - int((start.red - end.red) * chosen_d),
                start.green - int((start.green - end.green) * chosen_d),
                start.blue - int((start.blue - end.blue) * chosen_d)
            )

    im = Image.new(mode='RGB', size=(x, y))

    huy = random.random()
    huy2 = huy + 0.8
    if huy2 > 1:
        huy2 = huy2 - 1

    c1 = _hsv_to_rgb(huy, 1, 120)
    c2 = _hsv_to_rgb(huy2, 0.6, 250)

    color1 = RGBColor(*c1)
    color2 = RGBColor(*c2)

    shapes = _generate_triangles(int(x * 1.2), int(y * 1.2), int(x / 5))
    colors = random_color(color1, color2)
    for shape, color in zip(shapes, colors):
        ImageDraw.Draw(im).polygon(shape, fill=color)

    return im


def get_random_position():
    jobs = [
        'Certified Financial Planner',
        'Chartered Wealth Manager',
        'Credit Analyst',
        'Credit Manager',
        'Financial Analyst',
        'Hedge Fund Manager',
        'Hedge Fund Principal',
        'Hedge Fund Trader',
        'Investment Advisor',
        'Investment Banker',
        'Investor Relations Officer',
        'Leveraged Buyout Investor',
        'Loan Officer',
        'Mortgage Banker',
        'Mutual Fund Analyst',
        'Portfolio Management Marketing',
        'Portfolio Manager',
        'Ratings Analyst',
        'Stockbroker',
        'Trust Officer',
    ]
    return random.choice(jobs)


def generate_random_comp_name():
    fake = Faker()
    return fake.company()


def generate_random_transaction_hash():
    return '0x%s' % binascii.b2a_hex(os.urandom(32)).decode()


def get_random_date(start, end):
    """Generate a random datetime between `start` and `end`"""
    return start + timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())),
    )
