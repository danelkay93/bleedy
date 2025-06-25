export const processorSteps = [
  {
    name: 'Select Images',
    title: 'Select',
    iconName: 'image-selection-icon'
  },
  {
    name: 'Adjust Bleed',
    title: 'Settings',
    iconName: 'bleed-settings-icon'
  },
  {
    name: 'Process Images',
    title: 'Bleed!',
    iconName: 'blood-droplet-icon'
  },
  {
    name: 'Review Results',
    title: 'Results',
    iconName: 'stars-icon'
  }
] as const

export type ProcessorStep = (typeof processorSteps)[number]
