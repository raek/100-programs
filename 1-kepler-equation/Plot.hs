import Graphics.Rendering.Chart.Easy
import Graphics.Rendering.Chart.Backend.Cairo

signal :: [Double] -> [(Double,Double)]
signal xs = [ (x,(sin (x*3.14159/45) + 1) / 2 * (sin (x*3.14159/5))) | x <- xs ]

main = toFile def "kepler.png" $ do
    plot (points "M(E) (flipped)" (invFunPoints (meanAnomaly 0.5) [0,(0.1)..(2*pi)]))
    plot (line "E(M)" [funPoints (eccentricAnomaly 0.5) [0,(0.01)..(2*pi)]])

funPoints :: (Double -> Double) -> [Double] -> [(Double, Double)]
funPoints f xs = [(x, f x) | x <- xs]

invFunPoints :: (Double -> Double) -> [Double] -> [(Double, Double)]
invFunPoints f xs = [(f x, x) | x <- xs]

meanAnomaly :: Double -> Double -> Double
meanAnomaly eccentricity eccentricAnomaly =
  eccentricAnomaly - eccentricity * sin eccentricAnomaly

eccentricAnomaly :: Double -> Double -> Double
eccentricAnomaly eccentricity meanAnomaly =
  iterateUntilWithin next start epsilon
  where
    next = nextEccentricAnomaly eccentricity meanAnomaly
    start = meanAnomaly
    epsilon = 0.001

iterateUntilWithin :: (Double -> Double) -> Double -> Double -> Double
iterateUntilWithin next start epsilon = withinEpsilon approximations
  where
    withinEpsilon (a : xs@(b : _))
      | abs(a - b) <= epsilon = b
      | otherwise             = withinEpsilon xs
    approximations = iterate next start

nextEccentricAnomaly :: Double -> Double -> Double -> Double
nextEccentricAnomaly eccentricity meanAnomaly eccentricAnomaly =
  let x = eccentricAnomaly - eccentricity * sin eccentricAnomaly - meanAnomaly
      y = 1 - eccentricity * cos eccentricAnomaly
  in eccentricAnomaly - (x / y)
