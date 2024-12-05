#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def simple_kark_sort(s):
    # Keep track of original length
    n = len(s)
    # Append sentinel chars
    s += chr(1) * 3
    SA = [0]*(len(s))
    alpha = sorted(set(s))
    kark_sort(s, SA, n, alpha)
    # Return only the original sequence (without extra chars) and the first n elements of SA
    return s[:n], SA[:n]


def kark_sort(s, SA, n, alpha):
    n0 = (n + 2) // 3
    n1 = (n + 1) // 3
    n2 = n // 3
    n02 = n0 + n2

    # Positions of mod 1 and mod 2 suffixes
    s12 = [i for i in range(n + n0 - n1) if i % 3 != 0]
    s12 += [0, 0, 0]
    SA12 = [0]*(n02+3)

    # Radix sort on s12
    radixpass(s12, SA12, s[2:], n02, alpha)
    radixpass(SA12, s12, s[1:], n02, alpha)
    radixpass(s12, SA12, s, n02, alpha)

    # Assign ranks
    name = 0
    c0 = c1 = c2 = -1
    for i in range(n02):
        if (s[SA12[i]], s[SA12[i]+1], s[SA12[i]+2]) != (c0, c1, c2):
            name += 1
            c0 = s[SA12[i]]
            c1 = s[SA12[i]+1]
            c2 = s[SA12[i]+2]

        if SA12[i] % 3 == 1:
            s12[SA12[i]//3] = name
        else:
            s12[(SA12[i]//3)+n0] = name

    # Recurse if not all unique
    if name < n02:
        kark_sort(s12, SA12, n02, list(range(name+1)))
        for i in range(n02):
            s12[SA12[i]] = i + 1
    else:
        for i in range(n02):
            SA12[s12[i]-1] = i

    # Suffix array of mod 0
    s0 = [SA12[i]*3 for i in range(n02) if SA12[i]<n0]
    SA0 = [0]*n0
    radixpass(s0, SA0, s, n0, alpha)

    # Merge step
    p = 0
    t = n0 - n1
    k = 0

    while k < n:
        if t == n02:
            # Append remaining SA0 suffixes
            while p < n0:
                SA[k] = SA0[p]
                p += 1
                k += 1
            break
        if p == n0:
            # Append remaining SA12 suffixes
            while t < n02:
                pos = SA12[t]
                SA[k] = pos*3+1 if pos<n0 else (pos-n0)*3+2
                t += 1
                k += 1
            break

        # Compare suffixes
        pos12 = SA12[t]
        i = pos12*3+1 if pos12<n0 else (pos12-n0)*3+2
        j = SA0[p]

        if pos12 < n0:
            # Compare first char; if tie, compare ranks
            test = (s[i]<s[j]) or (s[i]==s[j] and s12[pos12+n0]<=s12[j//3])
        else:
            # mod-2 suffix
            if s[i]!=s[j]:
                test = (s[i]<s[j])
            else:
                # Compare next char if tie
                i1 = i+1
                j1 = j+1
                if s[i1]!=s[j1]:
                    test = s[i1]<s[j1]
                else:
                    test = s12[pos12 - n0 + 1]<=s12[(j//3)+n0]

        if test:
            SA[k] = i
            t += 1
        else:
            SA[k] = j
            p += 1
        k += 1

def radixpass(a, b, r, n, k):
    c = {}
    for lettre in k:
        c[lettre] = 0

    for i in range(n):
        c[r[a[i]]] += 1

    somme = 0
    for lettre in k:
        freq = c[lettre]
        c[lettre] = somme
        somme += freq

    for i in range(n):
        b[c[r[a[i]]]] = a[i]
        c[r[a[i]]] += 1

    return b

def LCP(s, suffix_array):
    n = len(s)
    rank = [0 for _ in range(n)]
    LCP = [0 for _ in range(n)]
    for i in range(n):
        rank[suffix_array[i]] = i
    l = 0
    for j in range(n):
        l = max(0, l - 1)
        i = rank[j]
        if i:
            j2 = suffix_array[i - 1]
            while l + j < n and l + j2 < n and s[j + l] == s[j2 + l]:
                l += 1
            LCP[i - 1] = l
        else:
            l = 0
    return LCP

if __name__ == '__main__':
    print("tools.py")
