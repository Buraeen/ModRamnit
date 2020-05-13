# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 12:38:24 2020

@author: Brian Akins
"""

import argparse
import random

class RandInt:

    def __init__(self, seed):
        self.value = seed

    def rand_int_modulus(self, modulus):
        ix = self.value
        ix = 16807*(ix % 127773) - 2836*(ix // 127773) & 0xFFFFFFFF
        self.value = ix
        return ix % modulus

def character_generator(r,choice):
    vowels = "aeiou"
    consonants = "bcdfghjklmnpqrstvwxyz"
    numbers = "1234567890"
    char = ""

    if choice != 0:
        if choice == 1:
            # Add a vowel.
            char = vowels[r.rand_int_modulus(5)]
        elif choice == 2:
            # Add a consonant.
            char = consonants[r.rand_int_modulus(21)]
        elif choice == 3:
            # Add a number.
            char = numbers[r.rand_int_modulus(10)]
    else:
        char = chr(ord('a') + r.rand_int_modulus(25))

    return char


def get_domains(seed, nr, tlds, maxLength, minLength, vowNum, conNum):
    if not tlds:
        tlds = [".com"]
    r = RandInt(seed)

    for i in range(nr):
        seed_a = r.value
        domain_len = r.rand_int_modulus(maxLength) + minLength
        seed_b = r.value
        domain = ""
        combinedRatio = vowNum+conNum

        for j in range(domain_len):
            if combinedRatio != 0:
                rand = random.random()
                if rand >= vowNum:
                    choice = 1
                elif rand <= conNum:
                    choice = 2
                else:
                    choice = 3
            else:
                choice = 0
            char = character_generator(r,choice)
            domain += char
        tld = tlds[i % len(tlds)]
        domain += '.' if tld[0] != '.' else ''
        domain += tld
        m = seed_a*seed_b
        r.value = (m + m//(2**32)) % 2**32
        yield domain

if __name__=="__main__":
    '''
    parser = argparse.ArgumentParser(description="generate Ramnit domains")
    parser.add_argument("seed", help="seed as hex")
    parser.add_argument("nr", help="nr of domains", type=int)
    parser.add_argument("-t", "--tlds", help="list of tlds", default=None)
    parser.add_argument("-xl", "--maxLength", help="Maximum domain length", default = 12, type=int)
    parser.add_argument("-nl", "--minLength", help="Minimum domain length", default = 8, type=int)
    parser.add_argument("-vn", "--vowNum", help="Number of vowels to use", type=float, default=0)
    parser.add_argument("-cn", "--conNum", help="Number of consonants to use", type=float, default=0)
    args = parser.parse_args()
    tlds = None
    maxLength = args.maxLength
    minLength = args.minLength
    vowNum = args.vowNum
    conNum = args.conNum
    '''
    tlds = None
    seed = "35F6AA8"
    nr = 300
    maxLength = 14
    minLength = 3
    vowNum = 0.7
    conNum = 0.6

    if tlds:
        tlds = [x.strip() for x in tlds.split(" ")]
    for domain in get_domains(int(seed, 16), nr, tlds, maxLength, minLength, vowNum, conNum):
        print(domain)