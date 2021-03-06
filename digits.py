import neural
import mnist


nn = neural.NeuralNetwork(28*28)
nn.add_layer(10)
n_iterations = 1


def from_mnist(label_file, image_file):
    labels = mnist.labels_from(label_file)
    images = mnist.images_from(image_file)
    for label, image in zip(labels, images):
        image = (pixel / 256. for pixel in image)
        expect = [0.]*label + [1.] + [0.]*(10-label)
        yield image, expect


print("training")
for _ in range(n_iterations):
    data = from_mnist("mnist/train-labels-idx1-ubyte.gz",
                      "mnist/train-images-idx3-ubyte.gz")
    for inputs, expect in data:
        nn.train(inputs, expect)

print("testing")
classifications = [[0]*10 for _ in range(10)]
data = from_mnist("mnist/t10k-labels-idx1-ubyte.gz",
                  "mnist/t10k-images-idx3-ubyte.gz")
for inputs, expect in data:
    # run neural network
    output = nn.compute(inputs)
    # recover labels
    output = output.index(max(output))
    expect = expect.index(max(expect))
    # account result
    classifications[expect][output] += 1

# show classifications
print("   " + " ".join("%4u" % label for label in range(10)))
for expect, row in enumerate(classifications):
    print("%u  " % expect + " ".join("%4u" % count for count in row))

# show overall result
n_tests = sum(sum(row) for row in classifications)
n_successes = sum(classifications[i][i] for i in range(10))
print("%u / %u" % (n_successes, n_tests))
