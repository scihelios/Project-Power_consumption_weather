#include <iostream>
#include <unordered_map>
#include <vector>
#include <algorithm> 
using namespace std;

int main() 
{
  int n,k;
  cin>>n>>k;
  int arr[200][2];
  for(int i=0;i<n;i++)
    cin>>arr[i][0]>>arr[i][1];
  int dp[n+1][k+1][2][2];
  for(int i=0;i<=n;i++){
    for(int j=0;j<=k;j++){
      dp[i][j][0][0]=0;
      dp[i][j][0][0]=0;
      dp[i][j][0][0]=0;
      dp[i][j][0][0]=0;
    }
  }
  for(int i=1;i<=n;i++){
    for(int j=1;j<=k;j++){
      int temp = max(dp[i-1][j][0][1]+arr[i-1][0],dp[i-1][j][1][0]+arr[i-1][1]);
      dp[i][j][0][0] = max(dp[i-1][j][0][0]+arr[i-1][0]+arr[i-1][1],temp);
      dp[i][j][1][0] = max(dp[i-1][j-1][0][0]+arr[i-1][0]+arr[i-1][1],dp[i-1][j-1][1][0]+arr[i-1][1]);
      dp[i][j][0][1] = max(dp[i-1][j-1][0][0]+arr[i-1][0]+arr[i-1][1],dp[i-1][j-1][0][1]+arr[i-1][0]);
    }
  }
  cout<<dp[n][k];
}
