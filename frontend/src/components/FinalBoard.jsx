import React, { useState, useEffect } from 'react'
import { Container, Table } from '@mantine/core'

import { ReactComponent as Gold } from '../assets/gold_medal_icon.svg'
import { ReactComponent as Silver } from '../assets/silver_medal_icon.svg'
import { ReactComponent as Bronze } from '../assets/bronze_medal_icon.svg'

// finalBoard prop should be an array of objects, one for each player
function FinalBoard ({ finalBoard }) {
  const [sortedBoard, setSortedBoard] = useState([])

  useEffect(() => {
    const sorted = finalBoard?.sort((a, b) => { return b.score - a.score })
    setSortedBoard(sorted)
  }, [finalBoard])

  const background = (i) => {
    // if (i === 1) return '#e0c56e' // gold
    // if (i === 2) return '#d5d5d7' // silver
    // if (i === 3) return '#c5ab84' // bronze
    return ''
  }

  return (
      <Container size="xl" px="sm">
        {
          <Table>
            <thead>
              <tr>
                <th>Position</th>
                <th>Name</th>
                <th>Score</th>
                <th>Success Rate</th>
                <th>Longest Streak</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {
                sortedBoard?.map((player, index) => (
                  <tr key={player.player_id} style={{ backgroundColor: background(index + 1) }}>
                    {/* <td>{(index + 1) + '.'}</td> */}
                    <td>
                      { index === 0 && <Gold /> }
                      { index === 1 && <Silver /> }
                      { index === 2 && <Bronze /> }
                      { index >= 3 && (index + 1) + '.'}
                    </td>
                    <td>{player.name}</td>
                    <td>{player.score}</td>
                    <td>{player.success_ratio}</td>
                    <td>{player.longest_streak}</td>
                  </tr>
                ))
              }
            </tbody>
          </Table>
        }
      </Container>
  )
}

export default FinalBoard
