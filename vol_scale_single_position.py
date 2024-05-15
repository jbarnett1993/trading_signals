def calculate_position_size(fund_size, annual_vol_target, asset_vols):
  # Calculate the daily vol target
  daily_vol_target = (annual_vol_target/100) / (252 ** 0.5)

  # Calculate the daily risk budget
  daily_risk_budget = fund_size * daily_vol_target

  # Calculate the target risk contribution for each asset class
  target_contribution = daily_risk_budget / len(asset_vols)
  print(target_contribution)
  # Calculate the position size for each asset
  position_sizes = []
  for vol in asset_vols:
      position_sizes.append(target_contribution / (vol / (252 ** 0.5) / 100))

  # Return the list of position sizes
  return position_sizes

# Example usage
fund_size = 50000000  # $50 million starting fund size
annual_vol_target = 10  # 10% target vol
asset_vols = [16, 20]  # Asset vols

position_sizes = calculate_position_size(fund_size, annual_vol_target, asset_vols)


print(position_sizes)
