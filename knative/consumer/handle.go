package function

import (
	"context"
	"crypto/md5"
	"fmt"
	"math/rand"
	"net/http"
	"os"
)

const FILES_DIR = "/files"

// Handle an HTTP Request.
func Handle(ctx context.Context, res http.ResponseWriter, req *http.Request) {
	fmt.Println("Reading directory")
	files, err := os.ReadDir(FILES_DIR)
	if err != nil {
		res.WriteHeader(http.StatusInternalServerError)
		fmt.Println(err)
		fmt.Fprint(res, "Error reading files directory")
		return
	}
	fmt.Printf("Found %d files\n", len(files))

	if len(files) == 0 {
		msg := "No files to consume"
		fmt.Println(msg)
		fmt.Fprint(res, msg)
		return
	}

	// Choose a random file
	fileEntry := files[rand.Intn(len(files))]
	fileName := fileEntry.Name()
	filePath := FILES_DIR + "/" + fileName

	fmt.Printf("Reading file %s\n", fileName)
	contents, err := os.ReadFile(filePath)
	if err != nil {
		res.WriteHeader(http.StatusInternalServerError)
		fmt.Println(err)
		fmt.Fprintf(res, "Error reading file %s", fileName)
		return
	}

	fileSize := len(contents)
	fmt.Printf("Read %d bytes\n", fileSize)

	md5sum := md5.Sum(contents)
	fmt.Printf("The md5 sum is %x\n", md5sum)

	fmt.Printf("Removing file %s\n", fileName)
	err = os.Remove(filePath)
	if err != nil {
		res.WriteHeader(http.StatusInternalServerError)
		fmt.Println(err)
		fmt.Fprintf(res, "Error removing file %s", fileName)
		return
	}
	fmt.Println("File removed")

	fmt.Fprintf(res, "Consumed file %s \nFile size is %d \nThe md5 sum is %x", fileName, fileSize, md5sum)
}
