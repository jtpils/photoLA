# -*- coding: utf-8 -*-
"""
Module to process an images to estimate leaf area.
This module is designed to be called from the terminal/command prompt.

@author: Matheus Boni Vicari (matheus.boni.vicari@gmail.com)
"""

import calculate_LA as cLA
import argparse
import os
import cv2
import pandas as pd


def run_cmd():

    # Parsing arguments inputed in the command prompt/terminal.
    f = args.file
    area_ref = float(args.area_ref)
    out_folder = os.path.join(args.out_folder, '')

    # Obtaining file name without path.
    filename = os.path.basename(f)

    # Obtaining current date and generating output data filename.
    out_filename = out_folder + 'LeafArea_%s.csv' % filename

    # Initializing DataFrame to store estimated leaf areas.
    df = pd.DataFrame(columns=['Leaf Area'])

    # Reading current image.
    img = cv2.imread(f)

    print('Processing image: %s\n' % f)

    # Obtaining masked images with leaf and reference pixels.
    leaf_pixels, ref_pixels = cLA.process_img(img)
    # Saving images with leaf and reference pixels.
    cv2.imwrite(out_folder + filename[:-4] + '_ref.png', ref_pixels)
    cv2.imwrite(out_folder + filename[:-4] + '_leaf.png', leaf_pixels)

    # Calculating leaf area.
    LA = cLA.calculate_area(leaf_pixels, ref_pixels, area_ref)

    # Appending current leaf area to dataframe.
    df = df.append(pd.DataFrame(LA, columns=['Leaf Area'],
                                index=[filename]))
    print('Leaf area: %s\n' % LA)

    # Exporting dataframe as csv file.
    df.to_csv(out_filename)


if __name__ == "__main__":

    # Initializing parser.
    parser = argparse.ArgumentParser(description='Batch run photoLA over all\
 images inside a given folder.')

    # Addind all required arguments.
    parser.add_argument('-f', '--file', dest='file', help='Image file.')
    parser.add_argument('-r', '--area_ref', dest='area_ref', help='Reference\
 area.')
    parser.add_argument('-o', '--output_folder', dest='out_folder',
                        help='Folder to save the results.')
    # Parsing arguments into variable args.
    args = parser.parse_args()

    # Running batch processing.
    run_cmd()
