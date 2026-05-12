---
name: nasa-random-space-image
description: Fetch a truly random high-quality space image from NASA's Astronomy Picture of the Day (APOD) archive with title, explanation, and direct image URL.
author: Mahadev Gaonkar
version: 1.0.0
tags: [nasa, space, astronomy, image, apod, random]
---

# NASA Random Space Image

Fetches a random astronomy image from NASA's vast APOD archive (1995–present).


# How to use

Here is web URL to fetch list of images: `https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&count=10`

The response is in following format:
```
{"copyright":"Bill Keel \n(University of Alabama)\n1.1-meter Hall Telescope, \nLowell Observatory","date":"1996-03-16","explanation":"Spiral galaxy M90 is near the center of the Virgo Cluster of Galaxies - the closest cluster of galaxies to the our own Milky Way Galaxy. Also dubbed NGC 4569, this galaxy has a very compact and bright nucleus. Because of M90's proximity and motion inside the Virgo Cluster, M90 actually shows a blueshift - indicating that it is moving toward us rather than away. Most galaxies show a redshift which indicates that they move away from us. Calibrating exactly how redshift relates to distance would indicate a scale for our universe - a topic of much debate recently.    Information: The Scale of the Universe Debate in April 1996","hdurl":"https://apod.nasa.gov/apod/image/m90_keel.gif","media_type":"image","service_version":"v1","title":"Spiral Galaxy M90","url":"https://apod.nasa.gov/apod/image/m90_keel.gif"}
```

Download the image using curl command and save it to local disk. Also save the title, explanation and image name in a text file. Save all the files in workspace directory.