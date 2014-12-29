# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import subprocess

from pkg_resources import resource_filename


def obtener_diccionario(filename):
    with open(filename) as archivo:
        return [linea.decode('utf-8').rstrip('\n') for linea in archivo]


def ejecutar_comando(command):
    while True:
        try:
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            p.wait()
            return [linea.decode('utf-8') for linea in p.stdout.readlines()]
        except KeyboardInterrupt:
            raise
        except Exception:
            pass


def filtrar_segun_votacion(corpus):
    res = []
    for tweet in corpus:
        if tweet.es_humor:
            if tweet.votos > 0:
                porcentaje_humor = tweet.votos_humor / float(tweet.votos)
                if porcentaje_humor >= 0.60:
                    res.append(tweet)
                elif porcentaje_humor <= 0.30:
                    tweet.es_humor = False
                    res.append(tweet)
        else:
            res.append(tweet)
    return res


def get_stop_words():
    with open(resource_filename('clasificador.recursos.diccionarios', 'stop_words.txt')) as archivo:
        return {linea.strip() for linea in archivo}
