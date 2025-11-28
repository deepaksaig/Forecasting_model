import React from 'react'
import { Button, Stack, Typography, List, ListItem, ListItemText } from '@mui/material'
import api from '../utils/api'
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts'

const ForecastStep = ({ context }) => {
  const [forecast, setForecast] = React.useState(null)

  const handleRun = async () => {
    const fileId = context.upload?.fileId
    if (!fileId) return
    const response = await api.post(`/forecast/${fileId}`, {
      drug_name: context.discovery?.drug_name || 'Unknown',
      target_metric: 'units_sold',
      forecast_horizon: 12,
      use_exogenous: true
    })
    setForecast(response.data)
  }

  const data = forecast ? forecast.dates.map((d, idx) => ({ date: d, forecast: forecast.forecast[idx] })) : []

  return (
    <Stack spacing={2}>
      <Typography>Run the forecasting pipeline and visualize results.</Typography>
      <Button variant="contained" onClick={handleRun}>Run forecast</Button>
      {forecast && (
        <>
          <Typography>Best model: {forecast.model_name}</Typography>
          <Typography variant="body2">RMSE: {forecast.metrics.rmse?.toFixed(3)} | MAE: {forecast.metrics.mae?.toFixed(3)}</Typography>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" hide />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="forecast" stroke="#1976d2" />
            </LineChart>
          </ResponsiveContainer>
          <List>
            {forecast.forecast.map((f, idx) => (
              <ListItem key={idx}>
                <ListItemText primary={`${forecast.dates[idx]}: ${Number(f).toFixed(2)}`} />
              </ListItem>
            ))}
          </List>
        </>
      )}
    </Stack>
  )
}

export default ForecastStep
