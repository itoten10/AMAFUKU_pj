'use client'

import { useEffect, useRef } from 'react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { Route, HistoricalSpot } from '@/types'
import polyline from 'polyline'

interface MapViewProps {
  route: Route
  onSpotClick: (spot: HistoricalSpot) => void
}

export function MapView({ route, onSpotClick }: MapViewProps) {
  const mapRef = useRef<L.Map | null>(null)
  const mapContainerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!mapContainerRef.current || mapRef.current) return

    // Initialize map
    const map = L.map(mapContainerRef.current).setView(
      [(route.origin_lat + route.dest_lat) / 2, (route.origin_lng + route.dest_lng) / 2],
      10
    )

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
    }).addTo(map)

    mapRef.current = map

    return () => {
      if (mapRef.current) {
        mapRef.current.remove()
        mapRef.current = null
      }
    }
  }, [])

  useEffect(() => {
    if (!mapRef.current || !route) return

    // Clear existing layers
    mapRef.current.eachLayer((layer) => {
      if (layer instanceof L.Marker || layer instanceof L.Polyline) {
        layer.remove()
      }
    })

    // Decode and add route polyline
    const decodedPath = polyline.decode(route.polyline)
    const routePath = L.polyline(decodedPath, {
      color: 'blue',
      weight: 5,
      opacity: 0.7,
    }).addTo(mapRef.current)

    // Add origin marker
    const originIcon = L.divIcon({
      html: `<div class="flex items-center justify-center w-8 h-8 bg-green-500 rounded-full text-white">
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.293l-3-3a1 1 0 00-1.414 1.414L10.586 9.5H7a1 1 0 100 2h3.586l-1.293 1.293a1 1 0 101.414 1.414l3-3a1 1 0 000-1.414z" clip-rule="evenodd" />
        </svg>
      </div>`,
      className: 'custom-div-icon',
      iconSize: [32, 32],
      iconAnchor: [16, 16],
    })

    L.marker([route.origin_lat, route.origin_lng], { icon: originIcon })
      .bindPopup(`<b>出発地</b><br>${route.origin}`)
      .addTo(mapRef.current)

    // Add destination marker
    const destIcon = L.divIcon({
      html: `<div class="flex items-center justify-center w-8 h-8 bg-red-500 rounded-full text-white">
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
        </svg>
      </div>`,
      className: 'custom-div-icon',
      iconSize: [32, 32],
      iconAnchor: [16, 16],
    })

    L.marker([route.dest_lat, route.dest_lng], { icon: destIcon })
      .bindPopup(`<b>目的地</b><br>${route.destination}`)
      .addTo(mapRef.current)

    // Add historical spot markers
    route.historical_spots?.forEach((spot) => {
      const spotIcon = L.divIcon({
        html: `<div class="flex items-center justify-center w-8 h-8 bg-orange-500 rounded-full text-white">
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
          </svg>
        </div>`,
        className: 'custom-div-icon',
        iconSize: [32, 32],
        iconAnchor: [16, 16],
      })

      const marker = L.marker([spot.lat, spot.lng], { icon: spotIcon })
        .bindPopup(`
          <div class="p-2">
            <b>${spot.name}</b><br>
            ${spot.address || ''}<br>
            ${spot.description || ''}
            <br><br>
            <button class="quiz-btn bg-primary-600 text-white px-3 py-1 rounded text-sm" data-spot-id="${spot.id}">
              クイズに挑戦
            </button>
          </div>
        `)
        .addTo(mapRef.current)

      marker.on('popupopen', () => {
        const btn = document.querySelector(`.quiz-btn[data-spot-id="${spot.id}"]`)
        if (btn) {
          btn.addEventListener('click', () => onSpotClick(spot))
        }
      })
    })

    // Fit map to bounds
    mapRef.current.fitBounds(routePath.getBounds(), { padding: [50, 50] })
  }, [route, onSpotClick])

  return (
    <div ref={mapContainerRef} className="w-full h-full rounded-lg" />
  )
}