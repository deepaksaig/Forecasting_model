import React from 'react'
import { Button, Stack, TextField, Typography, List, ListItem, ListItemText } from '@mui/material'
import api from '../utils/api'

const DiscoveryStep = ({ context, onNext }) => {
  const [form, setForm] = React.useState({ drug_name: '', atc_class: '', indication: '' })
  const [suggestions, setSuggestions] = React.useState([])
  const [queries, setQueries] = React.useState([])

  const handleSuggest = async () => {
    const response = await api.post('/discovery/suggest', { ...form, country: 'UK' })
    setSuggestions(response.data.suggestions)
    setQueries(response.data.search_queries)
    onNext({ ...response.data, drug_name: form.drug_name })
  }

  return (
    <Stack spacing={2}>
      <Typography>Enter drug details to get AI-assisted external data suggestions.</Typography>
      <TextField label="Drug name" value={form.drug_name} onChange={(e) => setForm({ ...form, drug_name: e.target.value })} />
      <TextField label="ATC class" value={form.atc_class} onChange={(e) => setForm({ ...form, atc_class: e.target.value })} />
      <TextField label="Indication" value={form.indication} onChange={(e) => setForm({ ...form, indication: e.target.value })} />
      <Button variant="contained" onClick={handleSuggest}>Suggest drivers</Button>
      <List>
        {suggestions.map((s, idx) => (
          <ListItem key={idx} alignItems="flex-start">
            <ListItemText primary={`${s.category} (${s.recommended_frequency})`} secondary={`${s.description} – ${s.reason_for_relevance}`} />
          </ListItem>
        ))}
      </List>
      {!!queries.length && (
        <Typography variant="caption">Example queries: {queries.join('; ')}</Typography>
      )}
    </Stack>
  )
}

export default DiscoveryStep
