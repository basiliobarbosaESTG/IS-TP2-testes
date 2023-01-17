import React, { useEffect, useState } from "react";
import { LayerGroup, useMap } from "react-leaflet";
import { ObjectMarker } from "./ObjectMarker";
import axios from "axios";

function ObjectMarkersGroup() {
  const map = useMap();
  const [atlethe, setAtlethes] = useState([]);
  const [bounds, setBounds] = useState(map.getBounds());

  const getMarkersAtlethes = async () => {
    let response = await axios.get("http://localhost:20002/api/markerAtlethe/");
    return response;
  };

  function trocarObjeto(atlethe) {
    return atlethe[0];
  }

  function addImage(atlethe) {
    atlethe.properties.imgUrl =
      "https://cdn-icons-png.flaticon.com/512/6534/6534578.png";
  }

  function changeCoordinates(atlethe) {
    let lon = atlethe.geometry.coordinates[0];
    let lat = atlethe.geometry.coordinates[1];
    let coordinates = [lat, lon];
    atlethe.geometry.coordinates = coordinates;
    return atlethe;
  }

  useEffect(() => {
    let atlethesObj = [];

    getMarkersAtlethes().then((response) => {
      response.data.map((atlethe) => {
        atlethe = trocarObjeto(atlethe);
        atlethe = changeCoordinates(atlethe);
        addImage(atlethe);
        atlethesObj.push(atlethe);
      });
      setAtlethes(atlethesObj);
    });
  }, []);

  /**
   * Setup the event to update the bounds automatically
   */
  useEffect(() => {
    const cb = () => {
      setBounds(map.getBounds());
    };
    map.on("moveend", cb);

    return () => {
      map.off("moveend", cb);
    };
  }, []);

  /* Updates the data for the current bounds */
  useEffect(() => {
    console.log(`> getting data for bounds`, bounds);
  }, [bounds]);

  return (
    <LayerGroup>
      {atlethe.map((geoJSON) => (
        <ObjectMarker key={geoJSON.properties.id} geoJSON={geoJSON} />
      ))}
    </LayerGroup>
  );
}

export default ObjectMarkersGroup;
