#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Plot a FITS file with the possibility to zoom in and out and change the contrast
of the image. The script also prints the header of the file if the argument -d
is passed.

1> Click on the image to zoom in
2> Right click in zoomed image to center the zoom on the clicked point
3> Scroll to zoom in and out in the zoomed image
4> Adjust the contrast with the sliders

Usage: python plot_fits_v1.1.py <filename> [-d]

Arguments:
    filename: the FITS file to be plotted
    -d: print the header of the file

Example:
    python plot_fits_v1.1.py file.fits -d

Author: Grégory Sainton
Lab : Observatoire de Paris - LERMA
Date: 04/12/2023
Version: 1.1

This code is distributed under the MIT license :
https://opensource.org/licenses/MIT


"""
import sys, os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib import rcParams
from matplotlib import gridspec
from matplotlib import rc

from pprint import pprint

from astropy.io import fits
from astropy.wcs import WCS

# warnings off
import warnings
warnings.filterwarnings("ignore")

class cursor(object):
    """
        Class to add a cursor on the image and update the zoomed image
        and the profiles

    """
    def __init__(self, ax):
        self.ax = ax
        self.lx = ax.axhline(color='red', ls='dotted', lw=0.5)
        self.ly = ax.axvline(color='red', ls='dotted', lw=0.5)
        self.zoomed_data = full_img
        self.x_min, self.x_max = 0, full_img.shape[1]
        self.y_min, self.y_max = 0, full_img.shape[0]
        self.posx_zoom = self.x_max / 2
        self.posy_zoom = self.y_max / 2
        self.zoom_width = 250

        # text location in axes coords
        self.txt = ax.text(0.7, 0.9, '', transform=ax.transAxes)

    def update_profiles(self):
        """
            Function to update the profiles of the zoomed image

        """

        flux_profile_x = self.zoomed_data[int(self.posy_zoom)-self.y_min, :]
        flux_profile_y = self.zoomed_data[:, int(self.posx_zoom)-self.x_min]

        # get the x and y coordinates of the zoomed image
        x_vec = np.arange(self.x_min, self.x_max)
        y_vec = np.arange(self.y_min, self.y_max)
        
        
        ax5.cla()
        ax5.set_ylabel(f_unit, fontsize=6)
        ax5.plot(flux_profile_y, y_vec, color='blue', lw=1)
        ax5.set_xlim([min(flux_profile_y), max(flux_profile_y)*1.1])
        ax5.set_ylim([self.y_min, self.y_max])
        ax5.grid(color='black', ls='dotted')

        ax6.cla()
        ax6.set_xlabel(f_unit, fontsize=6)
        ax6.plot(x_vec, flux_profile_x, color='blue', lw=1)
        ax6.set_ylim([min(flux_profile_x), max(flux_profile_x)*1.1])
        ax6.set_xlim([self.x_min, self.x_max])
        ax6.grid(color='black', ls='dotted')

        # Update the vertical and horizontal lines on the zoom image
        ax_zoom.axvline(self.posx_zoom, color='red', ls='dotted', lw=0.5)
        ax_zoom.axhline(self.posy_zoom, color='red', ls='dotted', lw=0.5)
        if len(ax_zoom.patches)>0:
            ax_zoom.patches[-1].remove()
        # Keep the last to lines
        if len(ax_zoom.lines) > 2:
            ax_zoom.lines[0].remove()
            ax_zoom.lines[0].remove()

        fig.canvas.draw_idle()

    def update_zoom(self, x, y):
        """
            Function to update the zoomed image

            Arguments:
                x: x coordinate of the clicked point
                y: y coordinate of the clicked point

        """
        global x_center, y_center

        # Extract a zoomed-in region around the clicked point
        self.x_min, self.x_max = int(x - self.zoom_width / 2), int(x + self.zoom_width / 2)
        self.y_min, self.y_max = int(y - self.zoom_width / 2), int(y + self.zoom_width / 2)

        if x is None or y is None:
            x, y = x_center, y_center
        else:
            x_center, y_center = x, y

        # Ensure the zoomed-in region stays within the image boundaries
        self.x_min = max(self.x_min, 0)
        self.x_max = min(self.x_max, full_img.shape[1])
        self.y_min = max(self.y_min, 0)
        self.y_max = min(self.y_max, full_img.shape[0])

        # Update the zoomed-in image data with vmin and vmax clipping
        self.zoomed_data = full_img[self.y_min:self.y_max, self.x_min:self.x_max]

        # Update the zoomed-in image axis limits
        ax_zoom.set_xlim(self.x_min, self.x_max)
        ax_zoom.set_ylim(self.y_min, self.y_max)
        ax_zoom.imshow(self.zoomed_data, cmap='viridis', origin='lower',
                        vmin=vmin, vmax=vmax)
        # Redraw the zoomed-in image
        self.update_profiles()
        fig.canvas.draw_idle()

    def on_click(self, event):
        """
            Function to manage the zoomed image and the profiles while clicking
            on the main image or the zoomed image.
            Left click on the main image to zoom in
            Left click on the zoomed image plot profiles at the clicked point
            Right click on the zoomed image to center the zoom on the clicked point

            Arguments:
                event: mouse click event

        """

        if event.inaxes == ax_main:
            x, y = int(event.xdata), int(event.ydata)
            self.posx_zoom, self.posy_zoom = x, y
            ax_main.axvline(x, color='red', ls='dotted', lw=0.5)
            ax_main.axhline(y, color='red', ls='dotted', lw=0.5)
            
            if len(ax_main.patches)>0:
                ax_main.patches[-1].remove()
            # Keep the last to lines
            if len(ax_main.lines) > 2:
                ax_main.lines[0].remove()
                ax_main.lines[0].remove()
            
            self.update_zoom(x, y)
            
            rect = plt.Rectangle((x - self.zoom_width / 2, y - self.zoom_width / 2),
                                self.zoom_width, self.zoom_width, fill=False, color='red',
                                ls='dotted', lw=0.5)
            ax_main.add_patch(rect)
            # Remove previous rectangle
            if len(ax_main.patches) > 1:
                ax_main.patches[0].remove()

            fig.canvas.draw_idle()

        if event.inaxes == ax_zoom:
            x, y = int(event.xdata), int(event.ydata)
            self.posx_zoom, self.posy_zoom = x, y

            if event.button == 3:                     # right click
                self.x_center, self.y_center = x, y
                self.update_zoom(self.x_center, self.y_center)

            # Update the vertical and horizontal lines on the main image
            ax_main.axvline(x, color='red', ls='dotted', lw=0.5)
            ax_main.axhline(y, color='red', ls='dotted', lw=0.5)

            if len(ax_main.patches)>0:
                ax_main.patches[-1].remove()
            # Keep the last to lines
            if len(ax_main.lines) > 2:
                ax_main.lines[0].remove()
                ax_main.lines[0].remove()
            # add a rectangle on the main image
            rect = plt.Rectangle((x - self.zoom_width / 2, y - self.zoom_width / 2),
                                self.zoom_width, self.zoom_width, fill=False, color='red',
                                ls='dotted', lw=0.5)
            ax_main.add_patch(rect)
            # Remove previous rectangle
            if len(ax_main.patches) > 1:
                ax_main.patches[0].remove()

            self.update_profiles()
            fig.canvas.draw_idle()

    def mouse_move(self, event):
        if event.inaxes == ax_zoom:
            posx, posy = int(event.xdata), int(event.ydata)

            # update the line positions
            self.lx.set_ydata(posy)
            self.ly.set_xdata(posx)
            fig.canvas.draw_idle()
        elif event.inaxes == ax_hist:
            posx, posy = event.xdata, event.ydata
            # remove previous vertical line
            if len(ax_hist.lines) > 0:
                ax_hist.lines[0].remove()
            ax_hist.axvline(posx, color='red', ls='dotted', lw=0.5)
            # remove previous text
            if len(ax_hist.texts) > 0:
                ax_hist.texts[0].remove()
            ax_hist.text(0.7, 0.9, f"{posx:.2f}", transform=ax_hist.transAxes, 
                         fontsize=6, color='black', verticalalignment='center')

            fig.canvas.draw_idle()


    def on_scroll(self, event, base_scale = 2.):
        """
            Function to manage the zoomed image and the profiles while scrolling
            on the zoomed image.
            Scroll up to zoom in
            Scroll down to zoom out

            Arguments:
                event: mouse scroll event
                base_scale: zoom factor

        """

        cur_xlim = ax_zoom.get_xlim()
        cur_ylim = ax_zoom.get_ylim()
        cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
        cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
        cur_xrange = (self.x_max - self.x_min)*.5
        cur_yrange = (self.y_max - self.y_min)*.5
        
        xdata = event.xdata # get event x location
        ydata = event.ydata # get event y location
        self.posx_zoom, self.posy_zoom = xdata, ydata
        
        if event.button == 'up':
            # deal with zoom in
            scale_factor = 1/base_scale
            self.zoom_width = self.zoom_width * scale_factor
        elif event.button == 'down':
            # deal with zoom out
            scale_factor = base_scale
            self.zoom_width = self.zoom_width * scale_factor
        else:
            # deal with something that should never happen
            scale_factor = 1
        # set new limits
        ax_zoom.set_xlim([xdata - cur_xrange*scale_factor,
                    xdata + cur_xrange*scale_factor])
        ax_zoom.set_ylim([ydata - cur_yrange*scale_factor,
                    ydata + cur_yrange*scale_factor])
        
        # Update the zoomed-in image data with vmin and vmax clipping
                # get the current x and y limits
        self.x_min = int(xdata - cur_xrange*scale_factor)
        self.x_max = int(xdata + cur_xrange*scale_factor)
        self.y_min = int(ydata - cur_yrange*scale_factor)
        self.y_max = int(ydata + cur_yrange*scale_factor)

        
        # Ensure the zoomed-in region stays within the image boundaries
        self.x_min = max(self.x_min, 0)
        self.x_max = min(self.x_max, full_img.shape[1])
        self.y_min = max(self.y_min, 0)
        self.y_max = min(self.y_max, full_img.shape[0])
        
        self.zoomed_data = full_img[self.y_min:self.y_max, self.x_min:self.x_max]

        # Update rectangle on the main image
        if len(ax_main.patches)>0:
            ax_main.patches[-1].remove()
        # Keep the last to lines
        if len(ax_main.lines) > 2:
            ax_main.lines[0].remove()
            ax_main.lines[0].remove()
        # add a rectangle on the main image
        rect = plt.Rectangle((xdata - self.zoom_width / 2, ydata - self.zoom_width / 2),
                            self.zoom_width, self.zoom_width, fill=False, color='red',
                            ls='dotted', lw=0.5)
        ax_main.add_patch(rect)
        # Remove previous rectangle
        if len(ax_main.patches) > 1:
            ax_main.patches[0].remove()
        self.update_profiles()
        fig.canvas.draw_idle()


def update_contrast(val):
    
    global im_main, im_zoom

    # Update the vmin and vmax of the main and zoomed-in images
    vmin = slider_vmin.val
    vmax = slider_vmax.val

    im_main.set_clim(vmin=vmin, vmax=vmax)
    im_zoom.set_clim(vmin=vmin, vmax=vmax)
    
    # Update the histogram limits
    img2plot_cl = np.clip(full_img, vmin, vmax)
    # refresh the histogram
    ax_hist.clear()
    ax_hist.hist(img2plot_cl.flatten(), bins=100, color="blue", alpha=0.7)
    ax_hist.set_yscale('log')
    ax_hist.set_xlabel(f_unit)
    ax_hist.set_ylabel('# pixels')
    ax_hist.set_xlim(vmin, vmax)
    ax_hist.set_title('Histogram')
    ax_hist.grid(color='black', ls='dotted')
    fig.canvas.draw_idle()

def update_zoom_factor(val):
    # Update the zoom factor
    global zoom_factor
    zoom_factor = slider_zoom.val


if __name__ == '__main__':
    
    # Check if there a filename as argument
    if len(sys.argv) == 1:
        print("Usage: python plot_fits_v1.1.py <filename> [-d]")
        sys.exit()
    elif len(sys.argv) == 2:
        FITS_file = sys.argv[1]
        print(f"Reading the file: {FITS_file}")
    elif len(sys.argv) == 3:
        FITS_file = sys.argv[1]
        print(f"Reading the file: {FITS_file}")
    else:
        print("Usage: python plot_fits_v1.1.py <filename> [-d]")
        sys.exit()

    # Check if the file is a FITS file and is not empty
    if not os.path.isfile(FITS_file):
        print(f"The file {FITS_file} does not exist")
        sys.exit()
    elif os.path.getsize(FITS_file) == 0:
        print(f"The file {FITS_file} is empty")
        sys.exit()
    elif not FITS_file.endswith('.fits'):
        print(f"The file {FITS_file} is not a FITS file")
        sys.exit()

    # Open the file
    hdul = fits.open(FITS_file)
    full_img = np.squeeze(hdul[0].data)

    # Check if any of the argument is -d to print the header
    if '-d' in sys.argv:
        print(f"Header of the file: {FITS_file}")
        print(50*"=")
        # Print header
        pprint(hdul[0].header)
        print(50*"=")

    # get the flux unit
    f_unit = hdul[0].header['BUNIT']
    
    # WCS  
    wcs = WCS(hdul[0].header)
    wcs = wcs.dropaxis(2).dropaxis(2)

    # Free memory 
    hdul.close()

    ImageTitle    = FITS_file.split('/')[-1].split('.')[0]
    ImageDate     = "DATE: " + hdul[0].header['DATE'] + ' ' + hdul[0].header['TIMESYS']
    ImageTelescop = "TELESCOPE: "+ hdul[0].header['TELESCOP']

    rcParams['backend'] = 'TkAgg'

    # Initialize zoom parameters
    zoom_factor = 2.0
    zoom_width = 250

    # Initialize vmin and vmax parameters
    vmin_initial = full_img.min()
    vmax_initial = full_img.max()

    vmin = np.min(full_img)
    vmax = np.max(full_img)

    h, w = full_img.shape

    fig = plt.figure(figsize=(10, 10))
    fig.subplots_adjust(hspace=0.1, wspace=0.1)
    fig.tight_layout()

    # Main grid spec
    gs0 = gridspec.GridSpec(2,2, figure=fig, width_ratios=[2,1],
                            height_ratios=[2,1], wspace=0.15, hspace=0.15)


    gs00 = gridspec.GridSpecFromSubplotSpec(1,2, subplot_spec=gs0[0,:],
                                            wspace=0.2, width_ratios=[2,1])

    # Up part of the plot containing the image and the histogram
    ax_main = fig.add_subplot(gs00[0], projection=wcs)
    im_main = ax_main.imshow(full_img, cmap='viridis', origin='lower')
    ax_main.set_title(ImageTitle)
    ax_main.set_xlabel('RA')
    ax_main.set_ylabel('DEC')
    ax_main.grid(color='black', ls='dotted')
    # add the colorbar
    cb = plt.colorbar(im_main, ax=ax_main, pad=0.01)
    cb.set_label(f_unit)
    # change position of the colorbar
    pos = ax_main.get_position()
    pos1 = cb.ax.get_position()
    cb.ax.set_position([pos1.x0+0.01,pos.y0,pos1.width,(pos.height)*0.8])
    # change the size of the ticks
    cb.ax.tick_params(labelsize=6)
    cb.ax.set_ylabel(f_unit, rotation=270, fontsize=6, labelpad=10)
    
    # Histogram
    img2plot_cl = np.clip(full_img, vmin, vmax)

    ax_hist = fig.add_subplot(gs00[1])
    ax_hist.hist(full_img.flatten(), bins=100, color="blue", alpha=0.7)
    ax_hist.set_yscale('log')
    ax_hist.set_title("Histogram")
    ax_hist.set_xlabel(f_unit)
    ax_hist.set_ylabel('# pixels')
    ax_hist.set_xlim(vmin, vmax)
    ax_hist.grid(color='black', ls='dotted')

    # align histogram and image
    pos  = ax_main.get_position()
    pos1 = ax_hist.get_position()
    ax_hist.set_position([pos1.x0,(pos.y0) + pos.height*0.5, 
                          pos.width*0.5,pos.height*0.5])

    # Print date and telescope below the histogram as floating text
    ax_main.text(0.01, -0.12, f"{ImageDate}\n{ImageTelescop}", fontsize=6,
                 color='black', transform=ax_main.transAxes, 
                 verticalalignment='center')
    

    ## Down part of the zoomed image and the integrated signal
    gs01 = gs0[1,0].subgridspec(2, 2, width_ratios=[w,w*.2],
                                height_ratios=[h,h*.2],
                                wspace=0.2, hspace=0.2)

    # Zoomed image
    ax_zoom = fig.add_subplot(gs01[0,0], projection=wcs)
    im_zoom = ax_zoom.imshow(full_img, cmap='viridis', origin='lower')
    ax_zoom.set_xlabel('RA')
    ax_zoom.set_ylabel('DEC')
    ax_zoom.grid(color='white', ls='dotted')
    ax_zoom.set_title("Zoom")
    ax_zoom.title.set_position([-0.2, 1.05])
    # set x labels on top
    ax_zoom.xaxis.tick_top()
    ax_zoom.xaxis.set_label_position('top')
    ax_zoom.tick_params(labelsize=6)

    # Right plot
    ax5 = fig.add_subplot(gs01[0,1], sharey=ax_zoom)

    ax5.set_xlabel(f_unit, fontsize=6, labelpad=10)
    ax5.tick_params(labelsize=6)
    ax5.tick_params(axis='x', rotation=90)
    ax5.xaxis.set_label_position('top')
    ax5.yaxis.set_visible(False)
    ax5.grid(color='black', ls='dotted')

    # Botton plot
    ax6 = fig.add_subplot(gs01[1,0], sharex=ax_zoom)
    ax6.set_ylabel(f_unit, fontsize=6)
    ax6.tick_params(labelsize=6)
    ax6.xaxis.set_visible(False)
    ax6.grid(color='black', ls='dotted')

    # align the axes
    pos  = ax_zoom.get_position()
    pos1 = ax5.get_position()
    pos2 = ax6.get_position()
    ax5.set_position([pos1.x0-0.10,pos.y0,pos.width*0.2,pos.height])
    ax6.set_position([pos.x0,pos2.y0,pos.width,pos.height*0.2])

    # Add slider for contrast and zoom
    axcolor_vmin = 'lightgoldenrodyellow'
    axcolor_vmax = 'lightblue'
    axcolor_zoom = 'lightgreen'

    # Add the sliders below the ax_hist
    ax_slider_vmin = plt.axes([0.70, 0.56, 0.15, 0.04], facecolor=axcolor_vmin)
    ax_slider_vmax = plt.axes([0.70, 0.53, 0.15, 0.04], facecolor=axcolor_vmax)
    ax_slider_zoom = plt.axes([0.70, 0.50, 0.15, 0.04], facecolor=axcolor_zoom)

    ax_slider_vmin.xaxis.set_visible(False)
    ax_slider_vmin.yaxis.set_visible(False)
    ax_slider_vmax.xaxis.set_visible(False)
    ax_slider_vmax.yaxis.set_visible(False)

    slider_vmin = Slider(ax_slider_vmin, 'vmin', full_img.min(),
                        full_img.max(), valinit=vmin_initial, valstep=0.001)
    slider_vmax = Slider(ax_slider_vmax, 'vmax', slider_vmin.val+0.001,
                        full_img.max(), valinit=vmax_initial, valstep=0.001)
    slider_zoom = Slider(ax_slider_zoom, 'zoom', 1.0, 50.0,
                        valinit=zoom_factor)


    # Connect sliders to update function
    slider_vmin.on_changed(update_contrast)
    slider_vmax.on_changed(update_contrast)
    slider_zoom.on_changed(update_zoom_factor)

    # add the cursor
    cursor_main = cursor(ax_main)
    cursor_zoom = cursor(ax_zoom)

    # connect the cursor to the mouse movement
    fig.canvas.mpl_connect('motion_notify_event', cursor_main.mouse_move)
    fig.canvas.mpl_connect('button_press_event', cursor_main.on_click)
    fig.canvas.mpl_connect('button_press_event', cursor_zoom.on_click)
    fig.canvas.mpl_connect('scroll_event', cursor_zoom.on_scroll)

    plt.show()
