import json
import math
from pathlib import Path


crateres_file = Path("data/craters_visible.json")
with open(crateres_file, "r", encoding='utf-8') as f:
    CRATERES = json.load(f)
del CRATERES["--"]


class Calculator():

    @staticmethod
    def comput_distanceGeo(coord_1, coord_2, radius):
        """Docstring"""
        lat1, lon1 = coord_1
        lat2, lon2 = coord_2
        # https://www.movable-type.co.uk/scripts/latlong.html
        φ1 = lat1 * math.pi / 180
        φ2 = lat2 * math.pi / 180
        Δφ = (lat2-lat1) * math.pi / 180
        Δλ = (lon2-lon1) * math.pi / 180

        a = math.sin(Δφ/2) * math.sin(Δφ/2) + \
            math.cos(φ1) * math.cos(φ2) * \
            math.sin(Δλ/2) * math.sin(Δλ/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = radius*c # meter
        return  d/1000 # Kilometer
    
    @staticmethod
    def comput_degreeToKm(circumference, latitude=0):
        """For a latitude degree, let latitude to 0"""
        return circumference * (math.cos(math.radians(latitude)) / 360)

    @staticmethod
    def comput_focalReal(pixel_size, obj_sizeKm, obj_sizePx, obj_distance, latitude=0, longitude=0):
        """Docstring"""
        obj_sizePxRevised = Calculator._craterSize_PxRevised(
                                        latitude,
                                        longitude,
                                        obj_sizeKm
                                        )
        transition_value = ((obj_sizePxRevised / 2) / obj_sizePx ) / obj_distance
        in_degre = math.degrees(math.atan(transition_value))
        arc_second = ((in_degre * 2) * 3600) / 206.265
        return  round(pixel_size / arc_second)

    @staticmethod
    def _craterSize_PxRevised(latitude, longitude, crater_SizeKm):
        """Docstring"""
        longitude = Calculator.convert_180(longitude)
        meridian = math.sqrt(latitude**2 + longitude**2)
        meridian_rad = math.radians(meridian)
        return crater_SizeKm * math.cos(meridian_rad)
    
    @staticmethod
    def comput_sampling(pixel_size, focal):
        """Docstring"""
        return pixel_size / focal * 206.265

    @staticmethod
    def comput_craterSize(datas :dict) -> dict:
        """datas = {
            "focal"         : int, float,
            "pixel_size"    : int, float,
            "pixel_number"  : int, float,
            "moon_distance" : int, float,
            "latitude"      : int, float,
            "longitude"     : int, float
        }"""
        sampling = Calculator.comput_sampling(
                    datas['pixel_size'],
                    datas['focal']
                    )
        degres = sampling / 3600 / 2
        radians = math.radians(degres)
        tang = math.tan(radians)
        inexact_craterSize = tang * datas['moon_distance'] * datas['pixel_number'] * 2
        crater_size = Calculator._craterSize_KmRevised(
                                                datas['latitude'],
                                                datas['longitude'],
                                                inexact_craterSize
                                                )
        return {
            'crater_size': inexact_craterSize,
            'crater_sizeP': crater_size,
            'sampling': sampling
            }
            
    @staticmethod
    def _craterSize_KmRevised(latitude, longitude, inexact_craterSize):
        """Docstring"""
        longitude = Calculator.convert_180(longitude)
        meridian = math.sqrt(latitude**2 + longitude**2)
        meridian_rad = math.radians(meridian)
        return inexact_craterSize / math.cos(meridian_rad)

    @staticmethod
    def comput_coefBarlow(drawing, focal_barlow):
        """Docstring"""
        return (drawing / focal_barlow) + 1

    @staticmethod
    def comput_distanceOrth(positions: list) -> tuple:
        """Docstring"""
        # Point de depart.
        x0, y0 = positions[0][0], positions[0][1]
        # Point darriver.
        x1, y1 = positions[1][0], positions[1][1]
        return ((((x1 - x0)**2) + ((y1 - y0)**2) )**0.5)

    @staticmethod    
    def comput_splitterPower(aperture):
        """Docstring"""
        return 120 / aperture

    @staticmethod
    def comput_ratioFD(aperture, focal):
        """Docstring"""
        return focal / aperture

    @staticmethod
    def comput_ratioFDf(pixel_size):
        """Docstring"""
        return pixel_size * 3.48

    @staticmethod    
    def comput_planetDistance(focal, pixel_size, number_pixel, planet_size):
        """Docstring"""
        angle = pixel_size / focal * 206.265
        arc_second = angle * number_pixel
        in_degre = arc_second / 3600  # Arc-seconde to degre.
        in_radian = math.radians(in_degre)  # Degre to radian.
        tangent = math.tan(in_radian)  # Comput tangent.
        return ((planet_size / number_pixel) / tangent) * number_pixel

    @staticmethod    
    def Km_to_Ua(km):
        """Docstring"""
        return km / 149597870.7

    @staticmethod    
    def average_dist(mini, maxi):
        """Docstring"""
        return mini + (maxi - mini) / 2
    
    @staticmethod
    def crater_area(north, south, est, west, km_per_pixel=0):
        """
        Fonction qui retourn la base de donné apres avoir supprimé
        tout les cratères qui ne sont pas dans la zone geographique.
        km_per_pixel per d'enlever les craters qui font moins
        de 4pixels sur la photo
        """
        est = Calculator.convert_180(est)
        west = Calculator.convert_180(west)
        crater_area = {}
        for crater, caracts in CRATERES.items():
            if not (south < caracts['latitude'] < north):
                continue
            if not (est < Calculator.convert_180(caracts['longitude']) < west):
                continue
            if caracts['diameter'] < km_per_pixel*4:
                continue
            crater_area[crater] = caracts
        return crater_area


    @staticmethod
    def identificat_crater(diameter=0, longitude=0, latitude=0, bdd=CRATERES):
        """
        Fonction qui retourne tout les crateres de la BDD
        ayant des caractéristiques proche.
        Un pourcentage de correspondance est estimé.
        """
        # initilisation de la marge d'erreur.
        marge = 5  # si diametre=90, alors la marge est de 85->95.
        # Mise en forme des arguments sous dict.
        unknow = {
            'diameter': diameter,
            'longitude': Calculator.normalize(longitude),
            'latitude': latitude
            }
        # Amplitude de chaque valeur.
        gap = {
            'diameter': (0.01, 300),
            'longitude': (0, 360),
            'latitude': (0, 180)
        }
        if diameter:
            marging = range(int(diameter) - marge, int(diameter) + marge)
            _key = 'diameter'
        elif longitude:  # Si pas de diametre, longitude est utilisé.
            # Normalise chaque valeur de marge.
            below = Calculator.normalize(longitude-(marge//2))
            above = Calculator.normalize(longitude+(marge//2))
            r = [int(below), int(above)]  # Pour min/max.
            marging = range(min(r), max(r))
            _key = 'longitude'
        matchs = {crater:v.copy() for crater,v in bdd.items() if int(v[_key]) in marging}

        for match, caracts in matchs.items():
            del matchs[match]['approval']
            del matchs[match]['date']
            del matchs[match]['origin']

            for k, value in caracts.items():
                ref = unknow[k] if unknow[k] != 0 else value
                mini, maxi = gap[k]
                temp1 = Calculator.gap_normalized(ref, value, mini, maxi)
                matchs[match][k] = temp1

            matchs[match] = Calculator._average(caracts.values())

        return matchs

    @staticmethod
    def _average(caracts:list) -> float:
        """Docstring"""
        return round(sum(caracts) / len(caracts), 2)
        
    @staticmethod
    def gap_normalized(ref, value, mini=0, maxi=100) -> float:
        """return le pourcentage d'ecart"""
        diff = abs(ref - value)
        pc = (diff - mini) / abs((maxi - mini))
        return 100 - (pc*100)

    @staticmethod
    def normalize(value, mini=0, maxi=360):
        """return longitude on 0/360"""
        if value < mini:
            value += maxi
        elif value > maxi:
            value -= maxi
        return value

    @staticmethod  
    def convert_180(value):
        """return longitude on -180/180"""
        if -180 < value < 180:
            return value
        elif value < -180:
            return 180 - (abs(value) - 180)
        else:
            return (abs(value) - 180) - 180


if __name__ == '__main__':
    diameter = 0
    latitude = 0
    longitude = 80

    # Calculator.identificat_crater(diameter=diameter, latitude=latitude, longitude=longitude)
    values = [-10, 10, -90, 100, 270, 380]
    values = [-10, 10, -90, 100, 270, 380, 181, -181]
    for a in values:
        print(a, Calculator.convert_180(a))