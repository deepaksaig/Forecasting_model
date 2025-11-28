import React from 'react'
import { Button, Stack, Typography, Table, TableHead, TableRow, TableCell, TableBody } from '@mui/material'
import api from '../utils/api'

const RegressorStep = ({ context, onNext }) => {
  const [regressors, setRegressors] = React.useState([])

  const handleLoad = async () => {
    const fileId = context.upload?.fileId
    if (!fileId) return
    const response = await api.get(`/sales/regressors/${fileId}?target_metric=units_sold`)
    setRegressors(response.data.regressors)
    onNext(response.data)
  }

  return (
    <Stack spacing={2}>
      <Typography>Fetch mock regressors and review coverage/correlations.</Typography>
      <Button variant="contained" onClick={handleLoad}>Load regressors</Button>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell>Coverage</TableCell>
            <TableCell>Missing %</TableCell>
            <TableCell>Correlation</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {regressors.map(r => (
            <TableRow key={r.name}>
              <TableCell>{r.name}</TableCell>
              <TableCell>{r.coverage_start} – {r.coverage_end}</TableCell>
              <TableCell>{(r.missing_ratio * 100).toFixed(1)}%</TableCell>
              <TableCell>{r.correlation_with_target?.toFixed(3) || 'n/a'}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Stack>
  )
}

export default RegressorStep
