import React from "react";
import { MapContainer, TileLayer } from "react-leaflet";
//import ObjectMarkersGroup from "./ObjectMarkersGroup";
import ObjectMarkersAtlhetes from "./ObjectMarkersAtlhetes";
//<ObjectMarkersGroup/>
function ObjectsMap() {
  return (
    <MapContainer
      style={{ width: "100%", height: "100vh" }}
      center={[0, 0]}
      zoom={2}
      scrollWheelZoom={false}
    >
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      <ObjectMarkersAtlhetes />
    </MapContainer>
  );
}

export default ObjectsMap;
