#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import csv
import urllib.request
import sys
# import requests
import time
# http://pydoc.net/Python/transmissionrpc/0.9/transmissionrpc.client
import transmissionrpc
from cpasbien_variables import *


class PasswdDialect(csv.Dialect):
    """Object du module csv permettant la compatibilite avec notre fichier"""
    # Separateur de champ
    delimiter = ","
    # Separateur de ''chaine''
    quotechar = None
    # Gestion du separateur dans les chaines
    escapechar = None
    doublequote = None
    # Fin de ligne
    lineterminator = "\n"
    # Ajout automatique du séparateur de chaîne (pour ''writer'')
    quoting = csv.QUOTE_NONE
    # Ne pas ignorer les espaces entre le délimiteur de chaîne
    # et le texte
    skipinitialspace = False

def brute_primaire(categorie):
    """Req pour brute html pages de téléchargement"""
    try:
        pageAcceuil = urllib.request.urlopen('http://www.cpasbien.cm/view_cat.php?categorie=' + categorie)
    except:
        print("Erreur urllib Brute primaire")
        sys.exit(1)
    else :
        return pageAcceuil.read().decode("utf-8")

def brute_torrent(urlPageDl):
    """Req pour brute html page des torrents"""
    try:
        pageFilm = urllib.request.urlopen(urlPageDl)
    except:
        print("Erreur urllib Brute torrent")
        sys.exit(1)
    else:
        return pageFilm.read().decode("utf-8")
    
def extraction_liens_pages(categorie):
    """Extraction Liens des page contenant les torrent"""
    regexPageFilms = re.compile("(?P<url>http://www.cpasbien.cm/dl-torrent/" + categorie + "[^\s\"]+[.html$])")
    return regexPageFilms.findall(brute_primaire(categorie))

def extraction_liens_torrent(page):
    """Extraction Liens torrent"""
    # TODO : Rendre plus propre en évitant findall split si possible
    regexLienTorrent = re.compile("(?P<url>/telechargement[^\s]+[.torrent$])")
    lienTorrent = regexLienTorrent.findall(brute_torrent(page))
    lienTorrent = lienTorrent[0].split('/')
    return lienTorrent[-1]

def chargement_historique(categorie):
    """Récupération des torrents déja Télécharger"""
    # TODO : Vérifier la présence du fichier avant tous
    rowdata = list()
    if os.path.exists("%s/%s.csv" % (os.path.dirname(os.path.realpath(__file__)), categorie)): # Le fichier existe
        with open("%s/%s.csv" % (os.path.dirname(os.path.realpath(__file__)), categorie), 'r') as fileCSV:
            var_csv = csv.reader(fileCSV, PasswdDialect())
            for row in var_csv: # Formatage en liste de l'objet csv
                rowdata.append(row[1])
        fileCSV.close()
    return rowdata

def sauvegarde_historique(categorie, lienTorrent):
    """sauvegarde historique des Torrents"""
    with open("%s/%s.csv" % (os.path.dirname(os.path.realpath(__file__)), categorie), 'a') as fileEnd:
        writer = csv.writer(fileEnd, PasswdDialect())
        writer.writerow([time.strftime("%d/%m/%Y"), lienTorrent])
    fileEnd.close()

def telechargement_torrent(transmission, lienTorrent, emplacement):
    """ajout du torrent"""
    try:
        transmission.add_torrent("http://www.cpasbien.cm/telechargement/%s " % lienTorrent, paused = False, download_dir = emplacement)
    except:
        return False
    else:
        return True

def verif_pour_telechargement(lienTorrent, historique):
    """Verifie que le torrent n'est pas déja historise"""
    if lienTorrent in historique:
        return False
    return True
