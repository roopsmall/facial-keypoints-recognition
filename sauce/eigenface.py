from numpy import genfromtxt, savetxt, linalg, dot, ceil, floor, argsort
from PIL import Image, ImageDraw
import seaborn as sns

class run(object):

	def __init__(self, eigenvectors='../data/eigenvectors.csv', delimiter=','):
	
	
		try:
			self.eigenvectors = genfromtxt(eigenvectors, delimiter=delimiter)
		except:
			self.eigenvectors = None
			print 'It looks like you need to run PCA first'


		
	@staticmethod
	def pca(data_file_in, offset, data_file_out='../data/eigenvectors.csv', delimiter=',', use=500):
		
		try:
			data = genfromtxt(data_file_in, delimiter=delimiter)[:,offset:].T
			data = data[:,:use]
			print 'Calculating scatter matrix..'
			data = dot(data, data.T)
			print 'Calculating eigenvectors..'
			A, V = linalg.eigh(data)
			print 'Sorting..'
			args = argsort(A)
			V = V[:, args]
			savetxt(data_file_out, V, delimiter=delimiter)

			return True

		except Exception as e:
			print e
			return False



	def top_eigenvectors(self, N=10, face_shape=(96,96), image_out=None):

		
		try:
			topN = self.eigenvectors[:,-N:]

			if image_out is not None:
				for eachline in range(0,N):
        				face = topN[:,eachline]
        				mx, mn = max(vector), min(vector)
        				face = (face - mn)*255.0/mx
        				im = face.reshape(face_shape)
        				im = Image.fromarray(im).convert('RGB')
        				im.save(image_out.replace('.png','') + '_' + eachline + '.png')

			return topN

		except:
			return 1



	def reconstruct_face(self, face_vector, N=10, eigenvectors='../data/eigenvectors.csv', delimiter=',', face_shape=(96,96), image_out=None):


		try:
			topN = self.top_eigenvectors(N=N)
        		coefficients = [dot(face_vector.T, topN[i]) for i in range(0,N)]
        		reconstruction = coefficients*topN
        		reconstruction = sum(reconstruction, 1)
        		mx, mn = max(reconstruction), min(reconstruction)
        		reconstruction = (reconstruction - mn)*255./mx
        		im = reconstruction.reshape((96,96))
        		im = Image.fromarray(im).convert('RGB')
        		if image_out is not None:
				im.save(image_out.replace('.png','') + '.png')
			
			return im
			
		except:
			return 1



if __name__ == '__main__':


	faces_data_file = '../data/test.csv'
	num_faces = 10
	rows = 2
	cols = int(ceil(num_faces/float(rows)))

	# perform PCA, save results to CSV file	
	run.pca(data_file_in=faces_data_file, offset=1)
	
	# get some 10 faces and reconstruct them
	faces = genfromtxt(faces_data_file, delimiter=',')[:num_faces,1:]

	# instantiate (memorise the eigenvalues)
	eig = run()
	
	# plot
	sns.plt.figure()
	for i in range(num_faces):
	        sns.plt.subplot(rows, cols, i+1)
		sns.plt.imshow(eig.reconstruct_face(faces[i,:]))
	sns.plt.show()	
	
