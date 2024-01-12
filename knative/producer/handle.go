package function

import (
	"context"
	"crypto/md5"
	cryptoRand "crypto/rand"
	"fmt"
	"math/rand"
	"net/http"
	"os"
)

const FILES_DIR = "/files"

// Handle an HTTP Request.
func Handle(ctx context.Context, res http.ResponseWriter, req *http.Request) {
	// Generates a file between 5 and 15 MB
	fileSize := (rand.Intn(10) + 5) * 1000_000
	fmt.Printf("Generated file size will be %d", fileSize)

	fmt.Println("Generating random bytes")
	contents := make([]byte, fileSize)
	generatedSize, err := cryptoRand.Read(contents)
	if err != nil {
		res.WriteHeader(http.StatusInternalServerError)
		fmt.Println(err)
		fmt.Fprint(res, "Error generating random data")
		return
	}
	fmt.Printf("Generated %d random bytes", generatedSize)

	md5sum := md5.Sum(contents)
	fmt.Printf("The md5 sum is %x\n", md5sum)

	fileName := fmt.Sprintf("%x.bin", md5sum)
	filePath := FILES_DIR + "/" + fileName
	fmt.Printf("Writing file %s\n", fileName)
	err = os.WriteFile(filePath, contents, 0666)
	if err != nil {
		res.WriteHeader(http.StatusInternalServerError)
		fmt.Println(err)
		fmt.Fprintf(res, "Error writing to file %s", fileName)
		return
	}
	fmt.Printf("Wrote file %s\n", fileName)

	fmt.Fprintf(res, "Produced file %s \nFile size is %d \nThe md5 sum is %x", fileName, fileSize, md5sum)
}
