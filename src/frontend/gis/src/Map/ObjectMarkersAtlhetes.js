import React, { useEffect, useState } from 'react';
import { LayerGroup, useMap } from 'react-leaflet';
import { ObjectMarker } from "./ObjectMarker";
import axios from "axios";

function ObjectMarkersGroup() {

    const map = useMap();
    const [atlethe, setAtlethes] = useState([]);
    const [bounds, setBounds] = useState(map.getBounds());

    const getMarkersAtlethes = async () => {
        try {
            const response = await axios.get("http://localhost:20001//api/markerAtlethe/");
            setAtlethes(response.data);
        } catch (error) {
            console.log(error);
        }
    };

    const markersAtlethes = [
        {
            "geometry": {
                "coordinates": [
                    2.1774322,
                    41.3828939
                ],
                "type": "Point"
            },
            "properties": {
                "city": "Barcelona",
                "id": "7d50b94f-2cbc-4429-afcc-1904905833dd",
                "name": "A Dijiang",
                imgUrl: "https://cdn-icons-png.flaticon.com/512/6534/6534578.png"
            },
            "type": "Feature"
        }
    ];

    useEffect(() => {
        getMarkersAtlethes();
    }, []);

    /**
     * Setup the event to update the bounds automatically
     */
    useEffect(() => {
        const cb = () => {
            setBounds(map.getBounds());
        }
        map.on('moveend', cb);

        return () => {
            map.off('moveend', cb);
        }
    }, []);

    /* Updates the data for the current bounds */
    useEffect(() => {
        console.log(`> getting data for bounds`, bounds);
        setAtlethes(markersAtlethes);
    }, [bounds])

    return (
        <LayerGroup>
            {
                atlethe.map(geoJSON => <ObjectMarker key={geoJSON.properties.id} geoJSON={geoJSON} />)
            }
        </LayerGroup>
    );
}

export default ObjectMarkersGroup;
