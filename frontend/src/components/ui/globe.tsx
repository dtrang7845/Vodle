"use client";

import { useEffect, useRef } from "react";
import * as d3 from "d3";

export type GlobePoint = {
  latitude: number;
  longitude: number;
  votes?: number;
  country?: string | null;
};

interface RotatingEarthProps {
  width?: number;
  height?: number;
  className?: string;
  points?: GlobePoint[];
}

export default function RotatingEarth({
  width = 800,
  height = 600,
  className = "",
  points = [],
}: RotatingEarthProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const context = canvas?.getContext("2d");
    if (!canvas || !context) {
      return;
    }

    const size = Math.min(width, height);
    const dpr = window.devicePixelRatio || 1;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    context.setTransform(dpr, 0, 0, dpr, 0, 0);

    const radius = size * 0.42;
    const projection = d3
      .geoOrthographic()
      .scale(radius)
      .translate([width / 2, height / 2])
      .clipAngle(90);
    const path = d3.geoPath().projection(projection).context(context);
    const graticule = d3.geoGraticule10();
    const rotation: [number, number] = [0, -12];

    const render = () => {
      context.clearRect(0, 0, width, height);
      projection.rotate(rotation);

      context.beginPath();
      context.arc(width / 2, height / 2, radius, 0, Math.PI * 2);
      context.fillStyle = "hsl(210 22% 10%)";
      context.fill();
      context.strokeStyle = "hsl(210 16% 34%)";
      context.lineWidth = 1;
      context.stroke();

      context.beginPath();
      path(graticule);
      context.strokeStyle = "hsl(210 14% 55% / 0.28)";
      context.lineWidth = 0.8;
      context.stroke();

      points.forEach((point) => {
        const projected = projection([point.longitude, point.latitude]);
        if (!projected) {
          return;
        }

        const visible = d3.geoDistance(
          [point.longitude, point.latitude],
          [-rotation[0], -rotation[1]],
        ) < Math.PI / 2;
        if (!visible) {
          return;
        }

        const pointRadius = Math.min(10, 3 + Math.sqrt(point.votes ?? 1) * 2);
        context.beginPath();
        context.arc(projected[0], projected[1], pointRadius + 4, 0, Math.PI * 2);
        context.fillStyle = "hsl(173 80% 45% / 0.18)";
        context.fill();
        context.beginPath();
        context.arc(projected[0], projected[1], pointRadius, 0, Math.PI * 2);
        context.fillStyle = "hsl(173 80% 45%)";
        context.fill();
        context.strokeStyle = "hsl(0 0% 100% / 0.8)";
        context.lineWidth = 1;
        context.stroke();
      });
    };

    const timer = d3.timer(() => {
      rotation[0] += 0.25;
      render();
    });

    render();

    return () => timer.stop();
  }, [height, points, width]);

  return (
    <canvas
      ref={canvasRef}
      aria-label="Vote locations globe"
      className={`h-auto max-w-full rounded-md bg-background ${className}`}
    />
  );
}
