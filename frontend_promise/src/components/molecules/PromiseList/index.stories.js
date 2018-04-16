import React from 'react'
import { storiesOf } from '@kadira/storybook'
import { PromiseList } from 'components'

storiesOf('PromiseList', module)
  .add('default', () => (
    <PromiseList>Hello</PromiseList>
  ))
  .add('reverse', () => (
    <PromiseList reverse>Hello</PromiseList>
  ))
