# blackscholespricing
Simple Options pricing application developed in Python.

## Formula

The Black-Scholes pricing formula for a call option is given by:

### Call Option Price

\[
C = S_0 N(d_1) - K e^{-rt} N(d_2)
\]

### Put Option Price

\[
P = K e^{-rt} N(-d_2) - S_0 N(-d_1)
\]

### Where:

- \(C\) = Call option price
- \(P\) = Put option price
- \(S_0\) = Current price of the underlying asset
- \(K\) = Strike price of the option
- \(t\) = Time to expiration (in years)
- \(r\) = Risk-free interest rate (annualized)
- \(\sigma\) = Volatility of the underlying asset (annualized)
- \(N(d)\) = Cumulative distribution function of the standard normal distribution

### \(d_1\) and \(d_2\) are calculated as:

\[
d_1 = \frac{\ln\left(\frac{S_0}{K}\right) + \left(r + \frac{\sigma^2}{2}\right)t}{\sigma \sqrt{t}}
\]

\[
d_2 = d_1 - \sigma \sqrt{t}
\]
