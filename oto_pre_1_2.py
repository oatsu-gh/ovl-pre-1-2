#! /usr/bin/env python3
# coding: utf-8
# Copyright (c) 2020 oatsu
"""
oto.ini を編集して
オーバーラップ領域 : 先行発声領域 = 1 : 2
にする。

[機能]
1. 先頭音はスキップする。
2. 先行発声/オーバーラップ >= 1/2 以上のとき、1/2になるように左ブランクを調整する。

"""

import utaupy


def check_ratio(otoini):
    counter = 0
    for oto in otoini:
        ratio = oto.overlap / oto.preutterance
        if oto.alias.startswith('- '):
            continue
        if ratio > 0.5:
            print(f'[WARN] 0.5 より大 :\t{oto.alias}\t{ratio}')
            counter += 1
        elif ratio < 0.34:
            print(f'  [INFO] 0.34未満 : \t{oto.alias}\t{ratio}')
            counter += 1
    print(f'counter : {counter}')


def adjust_offset(otoini):
    """
    1. 先頭音はスキップする。
    2. 先行発声/オーバーラップ >= 1/2 以上のとき、1/2になるように左ブランクを調整する。
    """
    warn_counter = 0
    info_counter = 0
    for oto in otoini:
        ratio = oto.overlap / oto.preutterance
        if oto.alias.startswith('- '):
            continue
        if ratio > 0.5:
            warn_counter += 1
            print(f'[WARN] 0.5 より大 :\t{oto.alias}\t{ratio}', end='\t')
            dt =  (2 * oto.overlap) - oto.preutterance
            oto.offset += dt
            oto.overlap -= dt
            oto.preutterance -= dt
            oto.consonant -= dt
            oto.cutoff2 += dt
            try:
                ratio = oto.overlap / oto.preutterance
            except ZeroDivisionError as e:
                print(f'[[ERROR]] {e}\t{oto.values}')
            print(f'->\t{oto.alias}\t{ratio}')
        elif ratio < 0.34:
            info_counter += 1
            print(f'  [INFO] 0.34未満 : \t{oto.alias}\t{ratio}')
    # WARN と INFO の合計個数を表示
    print(f'counter : {warn_counter}')
    print(f'counter : {info_counter}')


def main():
    path_ini = input('path_ini: ')
    otoini = utaupy.otoini.load(path_ini)
    # check_ratio(otoini)
    adjust_offset(otoini)
    otoini.write('oto_result.ini')
    input('おわり')


if __name__ == '__main__':
    main()
