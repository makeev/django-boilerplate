import os
import random
import string
import binascii
import collections

from datetime import timedelta

import names

from faker import Faker
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
