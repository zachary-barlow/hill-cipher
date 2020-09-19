from django.shortcuts import render
import numpy as np
from egcd import egcd

alphabet = "abcdefghijklmnopqrstuvwxyz"

letter_to_index = dict(zip(alphabet, range(len(alphabet))))
index_to_letter = dict(zip(range(len(alphabet)), alphabet))
def main(request):
  return render(request, 'index.html', {})

def cipher(request):
  opt = ""
  if request.method == "POST":
    c_to = request.POST.get("type").lower()
    phrase = request.POST.get("phrase")
    key_phrase = request.POST.get("matrix")
    num = int(request.POST.get("num"))
    
    num = num if num > 0 else num*(-1)

    if c_to == "encrypt":
      opt = encrypt(phrase, key_phrase, num)
    else:
      opt = decrypt(phrase, key_phrase, num)

  return render(request, 'index.html',{"output": opt})


####################################################
def encrypt(phrase, key_phrase, n):
  """
  """
  phrase = phrase.upper().replace(' ','')
  mat = make_matrix(phrase, n, "num", "encrypt")
  enc = make_matrix(key_phrase, n, "num", "")
  str_ = ""
  for row in enc:
    for col in mat:
      str_ += convert((row @ col) % 26, "val")

  return str_

def decrypt(phrase, key_phrase, n):
  """
  """
  phrase = phrase.upper().replace(' ','')
  mat = np.transpose(make_matrix(phrase, n, "num", ""))
  enc = make_matrix(key_phrase, n, "num", "")

  str_ = ""
  det = int(np.round(np.linalg.det(enc)))
  if  det != 0:
    k_inv= m_inv(enc)
    for row in k_inv:
      for col in mat:
        str_ += convert(np.dot(row, col) % 26, "val")
  else:
    str_ = "Key matrix is invalid"
  
  return str_

def m_inv(M):
  det = int(np.round(np.linalg.det(M)))
  det_inv = egcd(det,26)[1] % 26
  k_inv = det_inv * np.round(det * np.linalg.inv(M)).astype(int) % 26
  return k_inv

def convert(val, c_to):
  """
  """ 
  num = (ord(val) - 65) if c_to == "num" else (chr(val + 65))
  return num

def make_matrix(phrase, n, c_to, conv):
  """
  """
  # add extra letters onto the word if it doesnt have enough
  if len(phrase)%n > 0 and conv == "encrypt":
    l = 'A' * (n - len(phrase)%n)
    phrase += l
  
  # make the matrix of numbers
  mat = [[convert(j,c_to) for j in phrase[i:i+n]] for i in range(0,len(phrase),n)]
  
  return np.array(mat, dtype=int)