# viennaPublicTransportQuery
Automated query of real-time public transportation data for the 'Wiener Linien'

This repository contains a little script which can be used to query the API of the Wiener Linien and automatically print the requested data on the screen. 

## How-to
1. You need to get an API key from the Wiener Linien, which can be requested [here](https://www.wien.gv.at/formularserver2/user/formular.aspx?pid=3b49a23de1ff43efbc45ae85faee31db&pn=B0718725a79fb40f4bb4b7e0d2d49f1d1). Be sure to use the "limited" API key for implementation and testing purposes. This key will limit your available queries to 100 per minute and prevents too many server requests. When your code is finally in production, you may use the unlimited key.
2. Adapt the `config.yaml` and specify your favorite stations. This [tool](https://till.mabe.at/rbl/), kindly provided by [Matthias  Bendel](https://mabe.at/), helps you to find the corresponding RBL to your favorite station.

## Credits
Pascal Klemenz - https://github.com/PKlempe/WienerLinienMonitor-for-RaspberryPi

City of Vienna - https://data.wien.gv.at
