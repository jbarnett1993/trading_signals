def calculate_position_size_with_correlation(fund_size, annual_vol_target, asset_vols, asset_correlations):
  
  daily_vol_target = (annual_vol_target/100) / (252 ** 0.5)

  # Calculate the daily risk budget
  daily_risk_budget = fund_size * daily_vol_target

 # Calculate the target risk contribution for each asset class
  target_contribution = daily_risk_budget / len(asset_vols)
 
   # Initialize a list to hold the adjusted position sizes
  adjusted_position_sizes = []

  # Loop over the assets and adjust their position sizes based on the correlations
  for i in range(len(asset_vols)):
    # Calculate the unadjusted position size for the asset

    position_sizes = target_contribution / (asset_vols[i]/ (252 ** 0.5) / 100)
    print(position_sizes)

    # Initialize the adjusted position size to the unadjusted size
    adjusted_position_size = position_sizes

    # Loop over the other assets to calculate the correlation adjustment
    for j in range(len(asset_vols)):
      # Skip the asset if it is the same as the current asset
      if i == j:
        continue

      # Calculate the correlation adjustment for the pair of assets
      correlation_adjustment = asset_correlations[i][j] * position_sizes

      # Adjust the position size based on the correlation
      adjusted_position_size -= correlation_adjustment

      # Add the adjusted position size for the asset to the list
      adjusted_position_sizes.append(adjusted_position_size)

  return adjusted_position_sizes

print(adjusted_position_sizes)


  # Example usage
fund_size = 50000000  # $50 million starting fund size
annual_vol_target = 10  # 10% target vol
asset_vols = [16, 25]  # Asset vols

asset_correlations = [[1.0, 0.5], 
                     [0.23, 1.0]]
                     
position_sizes = calculate_position_size_with_correlation(fund_size, annual_vol_target, asset_vols, asset_correlations)

print(position_sizes)  