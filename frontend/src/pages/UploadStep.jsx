import React from 'react'
import { Button, Stack, Typography, Alert } from '@mui/material'
import api from '../utils/api'

const UploadStep = ({ onNext }) => {
  const [file, setFile] = React.useState(null)
  const [message, setMessage] = React.useState('')

  const handleUpload = async () => {
    if (!file) return
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post('/sales/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    setMessage(response.data.message)
    onNext({ fileId: response.data.file_id, uploadResponse: response.data })
  }

  return (
    <Stack spacing={2}>
      <Typography>Select a CSV with date, drug_name, units_sold, sales_value.</Typography>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <Button variant="contained" onClick={handleUpload}>Upload</Button>
      {message && <Alert severity="info">{message}</Alert>}
    </Stack>
  )
}

export default UploadStep
