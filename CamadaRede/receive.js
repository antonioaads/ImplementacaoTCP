const { readFileSync, writeFileSync } = require('fs')
const { execSync } = require('child_process')

const { loadConfig, extractFromEthPacket, isLocal, checkSum } = require('utils')

/**
 * args
 *  first 2 - unused args
 *  from 2 until the end - packets paths to be sent
 */
const args = process.argv.slice(2,process.argv.length)
const config = loadConfig()

function receiveNetworkPacket () {
  const packet = readFileSync(args[0]).toString()

  const fdestinationIp = extractFromEthPacket('final_destination_ip', packet)
  const destinationIp = extractFromEthPacket('destination_ip', packet)
  
  if (config.local.ip === fdestinationIp) {
    // save packet file and call transport layer
    saveAndPushUp(packet)
  } else {
    // decide next hop ip
    let nextHop = config.default

    if (isLocal(config.local.ip, config.local.mask, destinationIp)) {
      nextHop = destinationIp
    } else {
      for (const route in config.routes) {
        if (config.routes[route].includes(destinationIp)) {
          nextHop = route
          break
        }
      }
    }

    // save packet file and call physical layer
    saveAndResendPacket(packet, nextHop)
  }
}

function saveAndPushUp (originalPacket) {
  let packetFragments = originalPacket.split('||')
  let finalPacket = `||${packetFragments[3]}||`
  packetFragments = packetFragments.slice(4, packetFragments.length)
  packetFragments.forEach(frag => {
    finalPacket = `${finalPacket}${frag}`
  })

  writeFileSync('../pacotes/pud-volta.txt', finalPacket)
}

function saveAndResendPacket (originalPacket, nextHop) {
  const originIp = extractFromEthPacket('origin_ip', originalPacket)
  const packetCheckSum = extractFromEthPacket('checksum', originalPacket)
  let networkHeader = `||${originIp}|${nextHop}|${packetCheckSum}||`
  const finalPacket = `${networkHeader}${originalPacket}`

  writeFileSync('../pacotes/pdu_fisica.txt', finalPacket)
  execSync('../camada-fisica/cliente/cliente_fisica.sh')
}

receiveNetworkPacket()
