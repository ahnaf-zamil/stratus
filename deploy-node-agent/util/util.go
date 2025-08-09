package util

import (
	"crypto/rand"
	"encoding/hex"
)

func GenerateCryptoID() string {
	bytes := make([]byte, 8)
	if _, err := rand.Read(bytes); err != nil {
		panic(err)
	}
	return hex.EncodeToString(bytes)
}
