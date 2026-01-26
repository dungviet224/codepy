#include <bits/stdc++.h>
using namespace std;

bool is_prime(long long n){
    if(n < 2) return false;
    if(n == 2 || n == 3) return true;
    if(n % 2 == 0 || n % 3 == 0) return false;

    for(long long i = 5;i * i <= n;i += 6){
        if(n % i == 0 || n % (i + 2) == 0) return false;
    }
    return true;
}

bool ktra_so_uoc_nto(long long n){
    long long cnt = 0;
    for(int i = 1;i <= sqrt(n);i++){
        if(n % i == 0){
            cnt += 1;
            if(i != n / i){
                cnt += 1;
            }
        }
    }
    return is_prime(cnt);

}

int main() {
    vector<long long> prefix(1000009,0);

    for(long long i = 1;i <= 1000000;i++){
        if(ktra_so_uoc_nto(i)){
            prefix[i] = prefix[i - 1] + 1;
        }else{
            prefix[i] = prefix[i - 1];
        }
    }

    long long t; cin >> t;
    while(t--){
        long long a,b; cin >> a >> b;
        if(a == 0) a++;
        cout << prefix[b] - prefix[a - 1] << "\n";
    }
    return 0;
}