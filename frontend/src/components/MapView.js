import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';

const MapView = ({ data }) => (
  <div className="map-container">
    <MapContainer center={[20.59, 78.96]} zoom={5} style={{ height: '100%', width: '100%' }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {data.map((d, i) => (
        <Marker key={i} position={[d.latitude, d.longitude]}>
          <Popup>{d.district_name}<br/>Cluster: {d.cluster}</Popup>
        </Marker>
      ))}
    </MapContainer>
  </div>
);

export default MapView;
