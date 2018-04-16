import React from 'react'
import { storiesOf } from '@kadira/storybook'
import { AddPromise } from 'components'

storiesOf('AddPromise', module)
  .add('default', () => (
    <AddPromise>Hello</AddPromise>
  ))
  .add('reverse', () => (
    <AddPromise reverse>Hello</AddPromise>
  ))
