import React from 'react'
import { Container, Step, StepLabel, Stepper, Typography, Box, Paper } from '@mui/material'
import UploadStep from './pages/UploadStep'
import DiscoveryStep from './pages/DiscoveryStep'
import RegressorStep from './pages/RegressorStep'
import ModelingStep from './pages/ModelingStep'
import ForecastStep from './pages/ForecastStep'

const steps = ['Upload data', 'Driver suggestions', 'Regressors', 'Models', 'Forecast']

function App() {
  const [activeStep, setActiveStep] = React.useState(0)
  const [context, setContext] = React.useState({})

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        UK Pharma Sales Forecaster
      </Typography>
      <Stepper activeStep={activeStep} sx={{ mb: 3 }}>
        {steps.map(label => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>
      <Paper sx={{ p: 3 }}>
        {activeStep === 0 && <UploadStep onNext={(data) => { setContext({ ...context, upload: data }); setActiveStep(1) }} />}
        {activeStep === 1 && <DiscoveryStep context={context} onNext={(data) => { setContext({ ...context, discovery: data }); setActiveStep(2) }} />}
        {activeStep === 2 && <RegressorStep context={context} onNext={(data) => { setContext({ ...context, regressors: data }); setActiveStep(3) }} />}
        {activeStep === 3 && <ModelingStep context={context} onNext={(data) => { setContext({ ...context, modeling: data }); setActiveStep(4) }} />}
        {activeStep === 4 && <ForecastStep context={context} />}
      </Paper>
    </Container>
  )
}

export default App
