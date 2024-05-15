def calculate_position_size(fund_size, annual_vol_target, asset_vols, asset_correlations):
  # Calculate the daily vol target
  daily_vol_target = (annual_vol_target/100) / (252 ** 0.5)

  # Calculate the portfolio volatility
  portfolio_vol = 0
  for i in range(len(asset_vols)):
      for j in range(len(asset_vols)):
          portfolio_vol += asset_vols[i] * asset_vols[j] * asset_correlations[i][j]
  portfolio_vol = (portfolio_vol * 252) ** 0.5

  # Calculate the daily risk budget
  daily_risk_budget = fund_size * daily_vol_target / portfolio_vol

  # Calculate the target risk contribution for each asset class
  target_contribution = daily_risk_budget / len(asset_vols)
  print(target_contribution)

  # Calculate the position size for each asset
  position_sizes = []
  for vol in asset_vols:
      position_sizes.append(target_contribution / (vol / (252 ** 0.5) / 100))

  # Return the position sizes
  return position_sizes

fund_size = 50000000  # $50 million starting fund size
annual_vol_target = 10  # 10% target vol
asset_vols = [16, 25]  # Asset vols

asset_correlations = [[1.0, 0.5], 
                     [0.23, 1.0]]


position_sizes = calculate_position_size(fund_size, annual_vol_target, asset_vols, asset_correlations)

print(position_sizes)