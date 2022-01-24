def my_histogram_3d_plot(xticklabels, yticklabels, corr):
    
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    # Construct arrays for the anchor positions of the 16 bars.
    xpos, ypos = np.meshgrid([1,2,3,4], [1,2,3,4], indexing="ij")
    xpos = xpos.ravel()
    ypos = ypos.ravel()
    zpos = 0

    # Construct arrays with the dimensions for the 16 bars.
    dx = dy = 0.3
    dz = sum(corr, [])

    cmap = cm.get_cmap('jet')
    rgba = [cmap((k-min(dz))/max(dz)) for k in dz] 
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=rgba, zsort='average')

    ax.set_xticks([i + 1 for i in range(len(xticklabels))])
    ax.set_xticklabels(xticklabels)
    ax.set_yticks([i + 2 for i in range(len(yticklabels))])
    ax.set_yticklabels(yticklabels)

    ax.set_xlabel('factor 1')
    ax.set_ylabel('factor 2')
    ax.set_zlabel('correlation')
    ax.set_title('Correlation Map')

    plt.show()