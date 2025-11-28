import React from 'react'
import { Button, Stack, Typography, FormGroup, FormControlLabel, Checkbox } from '@mui/material'

const defaultModels = ['naive', 'moving_average', 'arima', 'random_forest']

const ModelingStep = ({ context, onNext }) => {
  const [selected, setSelected] = React.useState(defaultModels)

  const toggle = (model) => {
    setSelected(prev => prev.includes(model) ? prev.filter(m => m !== model) : [...prev, model])
  }

  return (
    <Stack spacing={2}>
      <Typography>Select which models to include in the comparison (mocked for now).</Typography>
      <FormGroup>
        {defaultModels.map(m => (
          <FormControlLabel key={m} control={<Checkbox checked={selected.includes(m)} onChange={() => toggle(m)} />} label={m} />
        ))}
      </FormGroup>
      <Button variant="contained" onClick={() => onNext({ models: selected })}>Continue</Button>
    </Stack>
  )
}

export default ModelingStep
