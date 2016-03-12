#!/usr/bin/python
# -*- coding: utf-8 -*-
from cpasbien_module import *
from cpasbien_variables import *
import transmissionrpc

#modification :
#06/02/2016 : suppression du telechargement des films VOSTFR

# TODO : Remplacer urllib par request

# Création de l'objet transmission
OBJ_transmission = transmissionrpc.Client(address = ADRESS_RPC, port = PORT_RPC, user = LOGIN_RPC, password = PASSWORD_RPC)

# Boucle par catégorie
for categorie in listeCategorie:
    historique = chargement_historique(categorie)
    # Boucles par page de téléchargement
    for urlPageDl in extraction_liens_pages(categorie):
        # TODO : Etape de vérification de la présence,
        lienTorrent = extraction_liens_torrent(urlPageDl)
        if verif_pour_telechargement(lienTorrent, historique):
            if categorie == 'films':
                if 'french' in lienTorrent.split('-'):
                    telechargement_torrent(OBJ_transmission, lienTorrent, DIR_FILMS + "FR")
                    sauvegarde_historique(categorie, lienTorrent)
                else:
                    telechargement_torrent(OBJ_transmission, lienTorrent, DIR_DEFAULT)
                    sauvegarde_historique(categorie, lienTorrent)
            if categorie == 'series':
                if 'vostfr' in lienTorrent.split('-'):
                    telechargement_torrent(OBJ_transmission, lienTorrent, DIR_SERIES + "VOSTFR")
                    sauvegarde_historique(categorie, lienTorrent)
                elif 'french' in lienTorrent.split('-'):
                    telechargement_torrent(OBJ_transmission, lienTorrent, DIR_SERIES + "FR")
                    sauvegarde_historique(categorie, lienTorrent)
                else:
                    telechargement_torrent(OBJ_transmission, lienTorrent, DIR_DEFAULT)
                    sauvegarde_historique(categorie, lienTorrent)
            if categorie == 'musique':
                telechargement_torrent(OBJ_transmission, lienTorrent, DIR_MUSIQUE)
                sauvegarde_historique(categorie, lienTorrent)
